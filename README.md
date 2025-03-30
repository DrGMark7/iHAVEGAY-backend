# iHAVEGAY Backend API

## Overview

This is the backend API for the iHAVEGAY Project, a computer hardware e-commerce platform that helps users find compatible computer components and build custom PCs.

## Prerequisites

- Python 3.8+
- MongoDB
- FastAPI

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/iHAVEGAY-backend.git
   cd iHAVEGAY-backend
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Start the MongoDB server:

   ```bash
   mongod --dbpath ~/database
   ```
4. Run the application:

   ```bash
   uvicorn app:app --reload
   ```

## Project Structure

```
iHAVEGAY-backend/
│
├── src/                        # Source code directory
│   ├── __init__.py             # Package initialization
│   ├── config.py               # Configuration settings
│   │
│   ├── controllers/            # Business logic layer
│   │   ├── admin_controller.py # Admin dashboard functionality
│   │   ├── auth_controller.py  # Authentication logic
│   │   ├── order_controller.py # Order management
│   │   ├── product_controller.py # Product management
│   │   └── user_controller.py  # User management
│   │
│   ├── database/               # Database configuration and connection
│   │   ├── __init__.py
│   │   └── database.py         # MongoDB connection setup
│   │
│   ├── models/                 # Data models and schemas
│   │   ├── __init__.py
│   │   ├── order_model.py      # Order data structures
│   │   ├── product_model.py    # Product data structures
│   │   └── user_model.py       # User data structures
│   │
│   ├── routes/                 # API routes and endpoints
│   │   ├── __init__.py
│   │   ├── admin_routes.py     # Admin dashboard endpoints
│   │   ├── auth_routes.py      # Authentication endpoints
│   │   ├── order_routes.py     # Order management endpoints
│   │   ├── product_routes.py   # Product endpoints
│   │   └── user_routes.py      # User management endpoints
│   │
│   ├── services/               # External service integrations
│   │   ├── __init__.py
│   │   ├── email_service.py    # Email notifications
│   │   └── payment_service.py  # Payment processing
│   │
│   └── utils/                  # Utility functions and helpers
│       ├── __init__.py
│       ├── auth_utils.py       # Authentication utilities
│       └── validators.py       # Input validation functions
│
├── app.py                      # Main application entry point
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## API Endpoints

The API is organized into the following main sections:

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/verify/{token}` - Verify email

### Products

- `GET /api/v1/products` - List all products
- `GET /api/v1/products/{product_id}` - Get product details
- `GET /api/v1/products/category/{category}` - Filter products by category

### Orders

- `POST /api/v1/orders` - Create a new order
- `GET /api/v1/orders/{order_id}` - Get order details
- `PUT /api/v1/orders/{order_id}/status` - Update order status

### Users

- `GET /api/v1/users/profile` - Get user profile
- `PUT /api/v1/users/profile` - Update user profile
- `GET /api/v1/users/orders` - Get user's order history

### Admin Dashboard

- `GET /api/v1/admin/sales/last-five-days` - Get sales data for the last 5 days
- `GET /api/v1/admin/inventory/low-stock` - Get products with low stock
- `GET /api/v1/admin/orders/recent` - Get recent orders
- `GET /api/v1/admin/inventory/summary` - Get inventory summary
- `GET /api/v1/admin/customers/top` - Get top customers
- `GET /api/v1/admin/products/top-selling` - Get top selling products
- `GET /api/v1/admin/products/compatible-mainboards/{cpu_id}` - Get compatible mainboards for CPU
- `GET /api/v1/admin/products/price-range` - Filter products by price range
- `GET /api/v1/admin/analytics/frequently-bought-together` - Get frequently bought together products
- `GET /api/v1/admin/products/recommended` - Get recommended budget products

## Database Structure

The application uses MongoDB with the following main collections:

- `users` - User accounts and profile information
- `orders` - Customer orders and transaction details
- `CPUs` - CPU product information
- `GPUs` - Graphics card product information
- `Rams` - RAM product information
- `Mainboards` - Motherboard product information
- `Cases` - PC case product information
- `PSUs` - Power supply product information
- `SSDs` - SSD storage product information
- `M2s` - M.2 storage product information

## Development

To start development:

1. Make sure MongoDB is running
2. Start the API server in development mode:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
3. Access the API documentation at: http://localhost:8000/docs

## Testing

Run tests with:

```bash
pytest
```

## License

This project is proprietary and confidential.

## Contributors

- Developer Team
