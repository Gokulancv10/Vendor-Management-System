
# Vendor Management Application

A RESTful API that provides vendor management functionality for any front-end application.


## 1. Project Setup

#### i. Clone the project into your local machine:

    git clone https://github.com/Gokulancv10/Vendor-Management-System.git

#### ii. Create a virtual environment and activate it:

    pip install virtualenv
	virtualenv env --python=python3
	source env/bin/activate (For Linux)
	env\Scripts\activate (For Windows)

#### iii. Install Dependencies:

	cd Vendor-Management-System
	pip install -r requirements.txt

## 2. Apply migrations

    python manage.py migrate

## 3. Run the development server

	python manage.py runserver

The server will run at http://127.0.0.1:8000

browse the URL http://127.0.0.1:8000/swagger/ All the APIs will be displayed

## API Reference

#### 1. List of all the vendors

```http
  GET /api/vendors/
```
| **Response**                                                           |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ```{[{ "id": 1, "name": "Rajesh", "contact_details": "+91-1234567899", "address": "No.1, 1st street, 1st city", "vendor_code": "1991", "on_time_delivery_rate": 0, "quality_rating_avg": 0, "average_response_time": 0, "fulfillment_rate": 0 }]}``` |

#### 2. Create a new vendor

```http
  POST /api/vendors/
```

| Payload | Response     | Description                       |
| :-------- | :------- | :-------------------------------- |
| ```{   "name": "Vinoth",   "contact_details": "+91-1234567890",   "address": "N0. 1/2, Abcd Street, XYZ",   "vendor_code": "1902" }```      | ```{   "id": 3,   "name": "Vinoth",   "contact_details": "+91-1234567890",   "address": "N0. 1/2, Abcd Street, XYZ",   "vendor_code": "1902",   "on_time_delivery_rate": 0,   "quality_rating_avg": 0,   "average_response_time": 0,   "fulfillment_rate": 0 }``` | Create new vendor |

#### 3. Retrieve vendor Detail

```http
  GET /api/vendors/{vendor_id}/
```
| Response |
| :------------- | 
| ```{   "id": 3,   "name": "Vinoth",   "contact_details": "+91-1234567890",   "address": "N0. 1/2, Abcd Street, XYZ",   "vendor_code": "1902",   "on_time_delivery_rate": 0,   "quality_rating_avg": 0,   "average_response_time": 0,   "fulfillment_rate": 0 }``` |


#### 4. Update a specific vendor’s details

```http
  PUT /api/vendors/{vendor_id}/
```

| Payload                                                                                                                            | Response                                                                                                                                                                                                                                                      |
|------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ```{   "name": "Vinoth K",   "contact_details": "+91-1234567890",   "address": "N0. 1/2, Abcd Street, XYZ",   "vendor_code": "1902" }``` | ```{   "id": 3,   "name": "Vinoth K",   "contact_details": "+91-1234567890",   "address": "N0. 1/2, Abcd Street, XYZ",   "vendor_code": "1902",   "on_time_delivery_rate": 0,   "quality_rating_avg": 0,   "average_response_time": 0,   "fulfillment_rate": 0 }``` |


#### 5. Delete a vendor
```http
  DELETE /api/vendors/{vendor_id}/
```

#### 6. Create a purchase order.
```http
  POST /api/purchase_orders/
```

| Payload | Response |
|---|---|
| ```{   "quantity": 2,   "vendor": 4,   "items": {           "product_id": "P002",           "product_name": "Desktop",           "unit_price": 1200         } }``` | ```{   "detail": {     "id": 4,     "po_number": "a6c05e93-f244-4857-9896-18d9bbedef2c",     "order_date": "2023-12-06T19:00:46.487105Z",     "delivery_date": "2023-12-10T19:00:46.487105Z",     "items": {       "product_id": "P002",       "product_name": "Desktop",       "unit_price": 1200     },     "quantity": 2,     "status": "PENDING",     "quality_rating": "0.00",     "issue_date": null,     "acknowledgment_date": null,     "vendor": {       "id": 4,       "name": "Abishek",       "contact_details": "+91-98279392",       "address": "No. 10, Venkatachalam street",       "vendor_code": "19863",       "on_time_delivery_rate": 0,       "quality_rating_avg": 0,       "average_response_time": 0,       "fulfillment_rate": 0     }   } }``` |


#### 7. List of purchase orders
```http
  GET /api/purchase_orders/
```

| Response                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ```{[{     "id": 1,     "po_number": "350bbebb-d9ca-45c7-bb5c-b96cbf1be492",     "order_date": "2023-12-06T18:52:54.466334Z",     "delivery_date": "2023-12-10T18:52:54.466334Z",     "items": {       "product_id": "P001",       "product_name": "Laptop",       "unit_price": 800     },     "quantity": 3,     "status": "PENDING",     "quality_rating": "0.00",     "issue_date": null,     "acknowledgment_date": null,     "vendor": {       "id": 3,       "name": "Vinoth K",       "contact_details": "+91-1234567890",       "address": "N0. 1/2, Abcd Street, XYZ",       "vendor_code": "1902",       "on_time_delivery_rate": 0,       "quality_rating_avg": 0,       "average_response_time": 0,       "fulfillment_rate": 0     }   }]}``` |


#### 8. Filter purchase orders by vendor
```http
  GET /api/purchase_orders/?vendor=1
```

| Response                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ```{[{     "id": 1,     "po_number": "350bbebb-d9ca-45c7-bb5c-b96cbf1be492",     "order_date": "2023-12-06T18:52:54.466334Z",     "delivery_date": "2023-12-10T18:52:54.466334Z",     "items": {       "product_id": "P001",       "product_name": "Laptop",       "unit_price": 800     },     "quantity": 3,     "status": "PENDING",     "quality_rating": "0.00",     "issue_date": null,     "acknowledgment_date": null,     "vendor": {       "id": 3,       "name": "Vinoth K",       "contact_details": "+91-1234567890",       "address": "N0. 1/2, Abcd Street, XYZ",       "vendor_code": "1902",       "on_time_delivery_rate": 0,       "quality_rating_avg": 0,       "average_response_time": 0,       "fulfillment_rate": 0     }   }]}``` |


#### 9. Delete a purchase order
```http
  DELETE /api/purchase_orders/{Purchase_Order_id}/
```


#### 10. Update a purchase order
```http
  PUT /api/purchase_orders/{Purchase_Order_id}/
```

| Payload                                              | Response                                                 |
|------------------------------------------------------|----------------------------------------------------------|
| ```{   "status": "COMPLETED",   "quality_rating": "3" } | {   "status": "COMPLETED",   "quality_rating": "5.00" }```  |

#### 11. Acknowledge purchase order
```http
  POST /api/purchase_orders/{Purchase_Order_id}/acknowledge/
```

| Response                                                              |
|-----------------------------------------------------------------------|
| ```{"detail": "The purchase order has been acknowledged successfully." }``` |

#### 12. Vendor performace metrics
```http
  GET /api/vendors/{Vendor_id}/performance/
```

| Response                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ```{   "id": 1,   "date": "2023-12-08T12:08:40.047494Z",   "average_response_time": 0.01191091013888889,   "average_response_time_in_hours": 0.28586184333333337,   "average_response_time_in_minutes": 17.1517106,   "average_response_time_in_seconds": 1029.102636,   "on_time_delivery_rate": 1,   "on_time_delivery_rate_percent": 100,   "quality_rating_avg": 3.0500000000000003,   "fulfillment_rate": 0.5,   "fulfillment_rate_percent": 50,   "vendor": {     "id": 1,     "name": "Abhishek",     "contact_details": "+91-12657",     "address": "JSHDishsdclkjcksdbcjksdchbsdkcj",     "vendor_code": "1000"   } }``` |



