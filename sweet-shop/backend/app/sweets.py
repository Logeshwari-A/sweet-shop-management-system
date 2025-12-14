from fastapi import APIRouter, Depends, HTTPException
from .schemas import SweetIn, SweetOut, PurchaseIn, RestockIn
from .db import sweets_collection
from .dependencies import get_current_user, get_admin_user
from bson import ObjectId

router = APIRouter(prefix="/api/sweets", tags=["sweets"])

@router.post("", response_model=SweetOut)
async def add_sweet(sweet: SweetIn, user=Depends(get_current_user)):
    doc = sweet.dict()
    res = await sweets_collection.insert_one(doc)
    doc_out = {"id": str(res.inserted_id), **doc}
    return doc_out

@router.get("", response_model=list[SweetOut])
async def list_sweets(user=Depends(get_current_user)):
    cursor = sweets_collection.find()
    items = []
    async for d in cursor:
        items.append({"id": str(d["_id"]), "name": d["name"], "category": d["category"], "price": d["price"], "quantity": d["quantity"]})
    return items

@router.get("/search", response_model=list[SweetOut])
async def search_sweets(name: str | None = None, category: str | None = None, min_price: float | None = None, max_price: float | None = None, user=Depends(get_current_user)):
    q = {}
    if name:
        q["name"] = {"$regex": name, "$options": "i"}
    if category:
        q["category"] = category
    if min_price is not None or max_price is not None:
        q["price"] = {}
        if min_price is not None:
            q["price"]["$gte"] = min_price
        if max_price is not None:
            q["price"]["$lte"] = max_price
    cursor = sweets_collection.find(q)
    items = []
    async for d in cursor:
        items.append({"id": str(d["_id"]), "name": d["name"], "category": d["category"], "price": d["price"], "quantity": d["quantity"]})
    return items

@router.put("/{id}", response_model=SweetOut)
async def update_sweet(id: str, sweet: SweetIn, user=Depends(get_current_user)):
    oid = ObjectId(id)
    res = await sweets_collection.find_one_and_update({"_id": oid}, {"$set": sweet.dict()}, upsert=False)
    if not res:
        raise HTTPException(status_code=404, detail="Sweet not found")
    new = await sweets_collection.find_one({"_id": oid})
    return {"id": str(new["_id"]), "name": new["name"], "category": new["category"], "price": new["price"], "quantity": new["quantity"]}

@router.delete("/{id}")
async def delete_sweet(id: str, admin=Depends(get_admin_user)):
    oid = ObjectId(id)
    res = await sweets_collection.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return {"deleted": True}

@router.post("/{id}/purchase")
async def purchase_sweet(id: str, purchase: PurchaseIn, user=Depends(get_current_user)):
    oid = ObjectId(id)
    res = await sweets_collection.find_one({"_id": oid})
    if not res:
        raise HTTPException(status_code=404, detail="Sweet not found")
    if res["quantity"] < purchase.amount:
        raise HTTPException(status_code=400, detail="Insufficient quantity")
    new_q = res["quantity"] - purchase.amount
    await sweets_collection.update_one({"_id": oid}, {"$set": {"quantity": new_q}})
    return {"id": id, "quantity": new_q}

@router.post("/{id}/restock")
async def restock_sweet(id: str, restock: RestockIn, admin=Depends(get_admin_user)):
    oid = ObjectId(id)
    res = await sweets_collection.find_one({"_id": oid})
    if not res:
        raise HTTPException(status_code=404, detail="Sweet not found")
    new_q = res["quantity"] + restock.amount
    await sweets_collection.update_one({"_id": oid}, {"$set": {"quantity": new_q}})
    return {"id": id, "quantity": new_q}
