# Vendor Management System

This Vendor Management System is designed to handle vendor profiles, track purchase orders, and calculate vendor performance metrics using Django and Django REST Framework.

## Setup Instructions

### Requirements
- Python 3.8+
- Django 3.2+
- Django REST Framework

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vendor_management.git
   cd vendor_management

2. Install the required packages:
    pip install -r requirements.txt


3. Run migrations to set up your database:
    python manage.py migrate

4. Start the development server:
    python manage.py runserver


# API Endpoints

## Vendor Endpoints
### Create a Vendor

    POST /api/vendors/
    Request Body:
    {
    "name": "Vendor Name",
    "contact_details": "Contact Information",
    "address": "Physical Address",
    "vendor_code": "UniqueVendorCode123"
    }


### List Vendors
    GET /api/vendors/

### Get Vendor Details
    GET /api/vendors/{vendor_id}/

### Update Vendor Details
    PUT /api/vendors/{vendor_id}/
    Request Body:
    {
    "name": "Updated Vendor Name",
    "contact_details": "Updated Contact Information",
    "address": "Updated Address"
    }

### Delete Vendor
    DELETE /api/vendors/{vendor_id}/


## Purchase Order Endpoints

### Create a Purchase Order
    POST /api/purchase_orders/
    Request Body:
    {
    "po_number": "PO123456",
    "vendor": 1,
    "order_date": "2021-01-01T00:00:00Z",
    "delivery_date": "2021-01-05T00:00:00Z",
    "items": {"item1": 10, "item2": 20},
    "quantity": 30,
    "status": "pending"
    }


### List all Purchase Orders
    GET /api/purchase_orders/

### Retrieve a specific Purchase Order
    GET /api/purchase_orders/{po_id}/


### Update a Purchase Order
    PUT /api/purchase_orders/{po_id}/
    Request Body:
    {
    "status": "completed"
    }


### Delete a Purchase Order
    DELETE /api/purchase_orders/{po_id}/

## Performance Metrics Endpoint

### Retrieve a Vendor's Performance Metrics
    GET /api/vendors/{vendor_id}/performance