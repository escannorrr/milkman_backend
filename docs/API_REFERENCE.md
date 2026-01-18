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

## 3. Route Operations
**Prefix**: **Unknown (Root/Default based on code inspection, assumed shared or root)**
*Note: `routing_routes.py` is likely included in `main.py` but currently I did not see it explicitly mounted in my previous read of `main.py`. If it's not mounted, these endpoints are inactive.*

### Create Route
- **URL**: `/create_route` (Check `main.py` for mount prefix, often `/api/v1/routes`)
- **Method**: `POST`
- **Body**:
  ```json
  {
    "routeName": "string",
    "dairyId": "string",
    "clients": ["string"]
  }
  ```
