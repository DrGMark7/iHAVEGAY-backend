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
├── main.py                     # Main application entry point
├── config.yaml                 # Configuration file
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
├── scrap.js                    # Scraping utilities
├── test                        # Test directory
│
└── src/                        # Source code directory
    ├── __init__.py             # Package initialization
    ├── config.py               # Configuration settings
    │
    ├── controllers/            # Business logic layer
    │   ├── __init__.py
    │   ├── admin_controller.py # Admin dashboard functionality
    │   ├── case_controller.py  # PC case management
    │   ├── cpu_controller.py   # CPU management
    │   ├── gpu_controller.py   # GPU management
    │   ├── mainboard_controller.py # Motherboard management
    │   ├── order_controller.py # Order management
    │   ├── psu_controller.py   # Power supply management
    │   ├── ram_controller.py   # RAM management
    │   └── storage_controller.py # Storage management
    │
    ├── database/               # Database configuration and connection
    │   ├── __init__.py
    │   ├── database.py         # MongoDB connection setup
    │   ├── manage_database.py  # Database management utilities
    │   └── json/               # JSON data files
    │
    ├── models/                 # Data models and schemas
    │   ├── __init__.py
    │   ├── hardware_models.py  # Hardware component models
    │   └── order_models.py     # Order data structures
    │
    ├── routes/                 # API routes and endpoints
    │   ├── __init__.py
    │   ├── admin_routes.py     # Admin dashboard endpoints
    │   ├── auth_routes.py      # Authentication endpoints
    │   ├── case_routes.py      # PC case endpoints
    │   ├── cpu_routes.py       # CPU endpoints
    │   ├── gpu_routes.py       # GPU endpoints
    │   ├── mainboard_routes.py # Motherboard endpoints
    │   ├── order_routes.py     # Order management endpoints
    │   ├── psu_routes.py       # Power supply endpoints
    │   ├── ram_routes.py       # RAM endpoints
    │   └── storage_routes.py   # Storage endpoints
    │
    ├── services/               # Service layer
    │   ├── __init__.py
    │   ├── hardware_service.py # Hardware component services
    │   └── order_service.py    # Order processing services
    │
    └── utils/                  # Utility functions and helpers
        ├── __init__.py
        └── auth.py             # Authentication utilities
```

## API Endpoints

The API is organized into the following main sections:

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - User login

### Hardware Components

#### CPUs

- `GET /api/v1/cpus` - Get all CPUs
- `GET /api/v1/cpus/{cpu_id}` - Get CPU by ID
- `POST /api/v1/cpus` - Create new CPU
- `PATCH /api/v1/cpus/{cpu_id}` - Update CPU by ID
- `DELETE /api/v1/cpus/{cpu_id}` - Delete CPU by ID

#### RAM

- `GET /api/v1/rams` - Get all RAM modules
- `GET /api/v1/rams/{ram_id}` - Get RAM by ID
- `POST /api/v1/rams` - Create new RAM
- `PATCH /api/v1/rams/{ram_id}` - Update RAM by ID
- `DELETE /api/v1/rams/{ram_id}` - Delete RAM by ID

#### Motherboards

- `GET /api/v1/mainboards` - Get all motherboards
- `GET /api/v1/mainboards/{mainboard_id}` - Get motherboard by ID
- `POST /api/v1/mainboards` - Create new motherboard
- `PATCH /api/v1/mainboards/{mainboard_id}` - Update motherboard by ID
- `DELETE /api/v1/mainboards/{mainboard_id}` - Delete motherboard by ID

#### GPUs

- `GET /api/v1/gpus` - Get all GPUs
- `GET /api/v1/gpus/{gpu_id}` - Get GPU by ID
- `POST /api/v1/gpus` - Create new GPU
- `PATCH /api/v1/gpus/{gpu_id}` - Update GPU by ID
- `DELETE /api/v1/gpus/{gpu_id}` - Delete GPU by ID

#### Cases

- `GET /api/v1/cases` - Get all PC cases
- `GET /api/v1/cases/{case_id}` - Get case by ID
- `POST /api/v1/cases` - Create new case
- `PATCH /api/v1/cases/{case_id}` - Update case by ID
- `DELETE /api/v1/cases/{case_id}` - Delete case by ID

#### Power Supplies (PSUs)

- `GET /api/v1/psus` - Get all power supplies
- `GET /api/v1/psus/{psu_id}` - Get PSU by ID
- `POST /api/v1/psus` - Create new PSU
- `PATCH /api/v1/psus/{psu_id}` - Update PSU by ID
- `DELETE /api/v1/psus/{psu_id}` - Delete PSU by ID

#### Storage (SSDs and M.2)

- `GET /api/v1/storage` - Get all storage devices
- `GET /api/v1/storage/{storage_id}` - Get storage by ID
- `POST /api/v1/storage` - Create new storage device
- `PATCH /api/v1/storage/{storage_id}` - Update storage by ID
- `DELETE /api/v1/storage/{storage_id}` - Delete storage by ID

### Orders

- `POST /api/v1/orders/create-with-details` - Create a new order
- `GET /api/v1/orders/{order_id}` - Get order by ID
- `PATCH /api/v1/orders/{order_id}/status` - Update order status
- `PATCH /api/v1/orders/{order_id}/shipping` - Update shipping details

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

## License

This project is proprietary and confidential.

## Contributors

- Napassakorn Saenieo
