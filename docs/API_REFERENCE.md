# Milkman Application API Reference

Base URL: `http://localhost:8000/api/v1`

## Authentication
Most endpoints generally require a Bearer Token (JWT).
- **Dairy Login**: Returns token for Dairy operations.
- **Milkman Login**: Returns token for Milkman operations.

---

## 1. Dairy Operations
**Prefix**: `/dairy`

### Signup
Register a new Dairy.
- **URL**: `/signup`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "dairyName": "string",
    "ownerName": "string",
    "phoneNumber": 0,
    "email": "string"
  }
  ```
- **Response**: Dairy Object

### Login
Login as a Dairy owner.
- **URL**: `/login`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "phoneNumber": 0,
    "password": "string"
  }
  ```
- **Response**: Dairy Object with Token

### Change Password
Change password for the authenticated Dairy.
- **URL**: `/change-password`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Body**:
  ```json
  {
    "oldPassword": "string",
    "newPassword": "string"
  }
  ```

---

## 2. Milkman Operations
**Prefix**: `/milkman`

### Create Milkman
Register a new Milkman under a Dairy.
- **URL**: `/create_milkman`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "milkmanName": "string",
    "dairyId": "string",
    "email": "string",
    "routeIdList": ["string"],
    "phoneNumber": 0,
    "adhaarNo": 0,
    "dl_number": "string"
  }
  ```
- **Response**: Milkman Object

### Get All Milkmen
Retrieve all milkmen associated with the authenticated Dairy.
- **URL**: `/get_all_milkman`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>` (Token from **Milkman** Login or **Dairy**? *Note: Logic implies this is a Dairy viewing their milkmen, but currently uses Milkman Auth schema in code - verification recommended*)
- **Response**:
  ```json
  {
    "milkMan": [ ...list of milkman objects... ]
  }
  ```

### Login
Login as a Milkman.
- **URL**: `/login`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "phoneNumber": 0,
    "password": "string"
  }
  ```
- **Response**: Milkman Object with Access Token

---

---

## 3. Route Operations
**Prefix**: `/routes`

### Create Route
- **URL**: `/create`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "routeName": "string",
    "dairyId": "string",
    "clients": ["string"]
  }
  ```
- **Response**: Route Object

### Get All Routes
- **URL**: `/all/{dairy_id}`
- **Method**: `GET`
- **Response**: List of Route Objects

### Update Route
- **URL**: `/{route_id}`
- **Method**: `PUT`
- **Body**:
  ```json
  {
    "routeName": "string" (optional),
    "clients": ["string"] (optional)
  }
  ```

### Delete Route
- **URL**: `/{route_id}`
- **Method**: `DELETE`

### Assign Milkman to Route
- **URL**: `/assign-milkman`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "routeId": "string",
    "milkmanId": "string"
  }
  ```

### Add Customers to Route
- **URL**: `/{route_id}/customers`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "clientIds": ["string", "string"]
  }
  ```


--- 

## 4. Customer Operations
**Prefix**: `/customers`

### Create Customer
- **URL**: `/create`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "customerName": "string",
    "dairyId": "string",
    "routeId": "string" (optional),
    "address": "string",
    "phoneNumber": integer,
    "dailyQuantity": float,
    "pricePerLiter": float
  }
  ```

### Get All Customers
- **URL**: `/all/{dairy_id}`
- **Method**: `GET`
- **Response**: List of Customer Objects

### Generate Bill (PDF)
- **URL**: `/generate-bill`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "customerId": "string",
    "startDate": "YYYY-MM-DD",
    "endDate": "YYYY-MM-DD"
  }
  ```
- **Response**: PDF File Download
