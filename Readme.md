# Form Builder

## Overview
**Form Builder** is a scalable web application designed for millions of users, enabling both admins and end-users to interact with forms seamlessly. Admin users can create new forms and view all forms created, while both admins and end-users can submit unlimited responses and access analytics. The analytics feature provides insights into form responses, including response counts and types, ensuring a user-friendly experience.

This project follows **SOLID principles**, ensuring a robust and scalable architecture. It includes features such as creating users, managing forms, submitting responses, and viewing analytics through well-defined REST API routes. PostgreSQL is used as the database to maintain the necessary associations and data integrity.

---

## Functionalities
1. **Create Form:** Admin users can create forms through the `/api/forms/` endpoint (query: `is_admin=true`).
2. **View All Forms:** Admin users can retrieve all forms created using the `/api/forms/list?user_id=<user_id>` endpoint.
3. **View Analytics:** Both admin and end-users can access form analytics, which shows response counts and types through the `/api/forms/<form_id>/analytics/` endpoint.
4. **Submit Responses:** Both admin and end-users can submit unlimited responses using the `/api/forms/<form_id>/responses/` endpoint.

---

## Features
- Designed following **SOLID principles** for maintainability and scalability.
- **Low-level design:** Class diagrams were used to design and create PostgreSQL tables with required associations.
- **Class diagram:**  
  https://drive.google.com/file/d/1vUmljohA06pXbIOZEwGf72Iy-29hO2YB/view?usp=sharing

- REST API routes are defined for all key functionalities:
  - **User Creation**: `/api/auth/create/`
  - **Form Creation**: `/api/forms/`
  - **Retrieve Forms**: `/api/forms/list?user_id=<user_id>`
  - **Submit Responses**: `/api/forms/<form_id>/responses/`
  - **Analytics**: `/api/forms/<form_id>/analytics/`
- Modular code base as per **Single Responsibility Principle** with comments for easier understanding.
- Scalable architecture designed in a three-tier setup. Future scalability can be achieved using cloud technologies such as **AWS EC2, AWS RDS, Nginx, and PM2**.

---

## Assumptions
- Admin users are identified by the `is_superuser` flag in the database.
- End-users can submit responses and view analytics but cannot create or manage forms.
- Forms can have multiple questions (up to 100), and questions can have multiple types (e.g., text, multiple choice).
- Analytics display includes response counts and breakdowns for each question type.
- The database configuration assumes a local PostgreSQL setup.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/PrathamAsrani/morpheus.git
cd morpheus
```

### 2. Create a Virtual Environment
```bash
python3 -m venv form_builder_env
```

### 3. Activate the Virtual Environment
- **Linux/MacOS:**
  ```bash
  source form_builder_env/bin/activate
  ```
- **Windows:**
  ```bash
  form_builder_env\Scripts\activate
  ```

### 4. Install Requirements
```bash
pip install -r requirements.txt
```

### 5. Initialize the Project
```bash
django-admin startproject form_builder
cd form_builder
```

### 6. Create the App
```bash
python manage.py startapp forms
```

### 7. Update `INSTALLED_APPS` in `settings.py`
Add the following:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # DRF
    'forms',  # Custom app
]
```

### 8. Configure PostgreSQL Database
Add your PostgreSQL credentials in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'form_builder_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 9. Run Migrations and Start Server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 10. View API Routes
```bash
python manage.py show_urls
```

---

## Testing with Postman

### Create a User
**Endpoint:** `POST /api/auth/create/`  
**Sample Request:**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "securepassword",
  "isAdmin": true
}
```

### Create a Form
**Endpoint:** `POST /api/forms/`  
**Authorization:** Requires admin credentials.  
**Sample Request:**
```json
{
  "title": "Survey Form",
  "questions": [
    {
      "text": "What is your favorite color?",
      "question_type": "text",
      "options": null
    },
    {
      "text": "Choose your hobbies",
      "question_type": "multiple_choice",
      "options": ["Reading", "Traveling", "Gaming"]
    }
  ]
}
```

### Submit Responses
**Endpoint:** `POST /api/forms/<form_id>/responses/`  
**Sample Request:**
```json
{
  "responses": [
    {
      "question_id": 1,
      "answer_text": "Blue"
    },
    {
      "question_id": 2,
      "selected_option": "Reading"
    }
  ]
}
```

### View Analytics
**Endpoint:** `GET /api/forms/<form_id>/analytics/`

---

## Future Enhancements
- Add frontend for better user interaction.
- Implement load balancing using AWS EC2 and RDS for improved scalability.
- Add caching mechanisms for faster performance.
- Ip caching to avoid DDoS attack