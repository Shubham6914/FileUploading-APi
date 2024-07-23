# Secure File Sharing System

This project is a secure file-sharing system implemented using Django REST Framework and MySQL. The system allows two types of users: Ops User and Client User, to perform specific actions.

## Features

### Ops User
- **Login**: Allows Ops User to log into the system.
- **Upload File**: Ops User can upload files of type `pptx`, `docx`, and `xlsx`.

### Client User
- **Sign Up**: Allows Client User to sign up and returns an encrypted URL.
- **Email Verify**: Sends a verification email to the registered email of the Client User.
- **Login**: Allows Client User to log into the system.
- **Download File**: Allows Client User to download files using a secure encrypted URL.
- **List All Uploaded Files**: Lists all files uploaded by Ops Users.

### Common
- **Register**: Allows any user to register.

## Important Information
- Only Ops Users are allowed to upload files.
- Files must be of type `pptx`, `docx`, and `xlsx`.
- Download URLs are encrypted and can only be accessed by Client Users.
- If any other user tries to access the URL, access is denied.

## Technology Stack
- **Framework**: Django REST Framework
- **Database**: MySQL
- **Testing Tool**: Postman

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/Shubham6914/FileUploading-APi.git
    cd FileUploading-APi
    ```

2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the MySQL database**
    - Create a database in MySQL.
    - Update the `DATABASES` settings in `settings.py` with your database credentials.

5. **Run migrations**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**
    ```bash
    python manage.py runserver
    ```

## Usage

- Use Postman to test the APIs. The following endpoints are available:
- All API endpoints start with `http://127.0.0.1:8000/user/`.

### Common Endpoints
- **Register**
    - `POST /user/register/`
    - Request Body: `{ "username": "new_user", "email": "new_user@example.com", "password": "password" }`

### Ops User Endpoints
- **Login**
    - `POST /user/ops/login/`
    - Request Body: `{ "username": "ops_user", "password": "password" }`

- **Upload File**
    - `POST /user/ops/upload/`
    - Request Body: `{ "file": <file> }`
    - Headers: `Authorization: Token <ops_user_token>`

### Client User Endpoints
- **Sign Up**
    - `POST /user/client/signup/`
    - Request Body: `{ "username": "client_user", "email": "client@example.com", "password": "password" }`

- **Email Verify**
    - `GET /user/client/verify-email/<verification_token>/`

- **Login**
    - `POST /user/client/login/`
    - Request Body: `{ "username": "client_user", "password": "password" }`

- **Download File**
    - `GET /user/client/download/<file_id>/`
    - Headers: `Authorization: Token <client_user_token>`

- **List All Uploaded Files**
    - `GET /user/client/files/`
    - Headers: `Authorization: Token <client_user_token>`

## Postman Collection
- A Postman collection for testing the APIs is included in the repository.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries, please contact [your_email@example.com].

