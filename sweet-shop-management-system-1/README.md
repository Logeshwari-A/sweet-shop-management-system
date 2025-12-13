# Sweet Shop Management System

## Overview
The Sweet Shop Management System is a full-stack application designed to manage the operations of a sweet shop. It consists of a React frontend, a FastAPI backend, and a MongoDB database. This system allows users to manage products, orders, and customers efficiently.

## Technologies Used
- **Frontend**: React, TypeScript
- **Backend**: Python, FastAPI
- **Database**: MongoDB
- **Containerization**: Docker

## Features
- **Product Management**: Create, read, update, and delete products.
- **Order Management**: Manage customer orders with CRUD operations.
- **Customer Management**: Maintain customer information and history.
- **Authentication**: Secure user authentication for accessing the system.

## Project Structure
```
sweet-shop-management-system
├── backend
│   ├── app
│   ├── tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
├── frontend
│   ├── package.json
│   ├── tsconfig.json
│   ├── public
│   ├── src
│   └── README.md
├── infra
│   └── mongo-init
│       └── init.js
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites
- Docker
- Docker Compose
- Node.js and npm
- Python 3.7 or higher

### Installation

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd sweet-shop-management-system
   ```

2. **Set up the backend**:
   - Navigate to the `backend` directory.
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```

3. **Set up the frontend**:
   - Navigate to the `frontend` directory.
   - Install dependencies:
     ```
     npm install
     ```

4. **Run the application**:
   - Use Docker Compose to start the application:
     ```
     docker-compose up
     ```

### Usage
- Access the frontend at `http://localhost:3000`.
- The backend API can be accessed at `http://localhost:8000/api/v1`.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.