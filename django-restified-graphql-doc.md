## Authentication Endpoints Documentation

This document describes two API endpoints in Django for user authentication: `sign_up` for user registration and `sign_in` for user login. These endpoints communicate with an external Hasura-based service to handle user data, leveraging JSON Web Tokens (JWT) for secure role-based access control.

### Prerequisites
- Python packages: `djangorestframework`, `requests`, and `pyjwt`.
- Environment variable `HASURA_SECRET_KEY` for signing JWTs.

---

## `sign_up` Endpoint

### URL
`POST /sign_up`

### Description
The `sign_up` endpoint registers a new user by receiving user details, validating them, and then forwarding them to an external API (`/api/rest/signup`). It generates a JWT for the newly created user to provide access to other Hasura-based services.

### Request Parameters
- **email** (string, required): User's email address.
- **first_name** (string, optional): User's first name.
- **last_name** (string, optional): User's last name.
- **phone_number** (string, required): User's phone number.
- **password** (string, required): User's password.

### Workflow
1. **Input Validation**: Checks if `email`, `phone_number`, and `password` are provided.
2. **Django JWT Generation**: Creates a token using a predefined role (`django`) for Hasura-based services.
3. **External API Call**: Sends a request with user details to `http://localhost:8080/api/rest/signup`.
4. **Response Handling**: 
   - If there is an error or the request fails, an appropriate error message is returned.
   - If the signup is successful, a second JWT is generated with user-specific roles and privileges.
5. **Return JWT**: Returns a JWT with user roles to the client.

### Example Request
```json
{
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "password": "SecurePassword123"
}
```

### Response
- **Success (201 Created)**:
  ```json
  {
      "token": "jwt_token"
  }
  ```
- **Error (400 Bad Request)**:
  ```json
  {
      "error": "Email, phone number, and password are required."
  }
  ```

---

## `sign_in` Endpoint

### URL
`POST /sign_in`

### Description
The `sign_in` endpoint authenticates an existing user by verifying their email and password. If successful, it generates a JWT with the user's roles and permissions, providing them access to Hasura services.

### Request Parameters
- **email** (string, required): User's email address.
- **password** (string, required): User's password.

### Workflow
1. **Input Validation**: Ensures both `email` and `password` are present.
2. **Django JWT Generation**: A Django server token is generated to authenticate with Hasura.
3. **External API Call**: Sends the email and password to `http://localhost:8080/api/rest/signin`.
4. **Response Handling**:
   - If there’s an error or failed authentication, an error is returned.
   - If successful, the endpoint retrieves the user’s details and assigns a `user` role.
5. **Return JWT**: Responds with a JWT token and user profile data.

### Example Request
```json
{
    "email": "user@example.com",
    "password": "SecurePassword123"
}
```

### Response
- **Success (200 OK)**:
  ```json
  {
      "user": {
          "id": "user_id",
          "first_name": "John",
          "last_name": "Doe",
          "phone_number": "1234567890",
          "email": "user@example.com",
          "address": "",
          "token": "jwt_token"
      }
  }
  ```
- **Error (400 Bad Request)**:
  ```json
  {
      "error": "Email and password are required."
  }
  ```

---

## Notes
- JWT tokens are signed with `ES256` using `HASURA_SECRET_KEY`.
- Both endpoints require a working Hasura API endpoint at `http://localhost:8080`.
- If the external service is unavailable, a 503 error is returned.