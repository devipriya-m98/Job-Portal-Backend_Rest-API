# Job Application Backend – REST API

A RESTful Job Application Backend developed using Django and Django REST Framework . This application allows recruiters to post and manage job opportunities, while candidates can create profiles, browse jobs, and apply for jobs.

## Features

### 1. User Authentication
- User registration and login.
- Token-based authentication.
- User roles: Recruiter and Candidate.
- Logout functionality.
- Input validation and error handling.

### 2. Job Management
- View all available jobs.
- View individual job details.
- Recruiters can create new jobs.
- Recruiters can update and delete their own jobs.
- Job status management (Open / Closed).
- Only recruiters can manage job postings.

### 3. Candidate Profile Management
- Create candidate profiles.
- View candidate profiles.
- Update candidate profiles.
- Partial profile updates.
- Only candidates can manage their own profiles.

### 4. Job Application Management
- Candidates can apply for jobs.
- Candidates can view their applications.
- Candidates can view individual application details.
- Prevent duplicate applications.
- Prevent applications for closed jobs.
- Recruiters can update application status for jobs they posted.

### 5. Application Status
Available application statuses:

- APPLIED
- SHORTLISTED
- INTERVIEW
- SELECTED
- REJECTED

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite
- Django Token Authentication
- REST API


## Installation and Setup

### 1. Clone the repository

git clone <your-github-repository-url>


### 2. Navigate to the project directory

cd "Job Application Backend_REST API"


### 3. Create a virtual environment

python -m venv .env

### 4. Activate the virtual environment

Windows PowerShell:
.env\Scripts\Activate


### 5. Install dependencies

pip install django djangorestframework


### 6. Apply migrations

python manage.py makemigrations
python manage.py migrate


### 7. Create a superuser

python manage.py createsuperuser

### 8. Run the development server

python manage.py runserver

The application will be available at:

http://127.0.0.1:8000/

## API Endpoints

Base URL:

`http://127.0.0.1:8000/api/`

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register/` | Register a new user |
| POST | `/login/` | Login user |
| POST | `/logout/` | Logout user |

### Job Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/jobs/` | View all jobs |
| POST | `/jobs/` | Create a job (Recruiter) |
| GET | `/jobs/<id>/` | View job details |
| PUT | `/jobs/<id>/` | Update a job |
| PATCH | `/jobs/<id>/` | Partially update a job |
| DELETE | `/jobs/<id>/` | Delete a job |

### Candidate Profile

| Method | Endpoint | Description |
|---|---|---|
| POST | `/candidate-profile/` | Create candidate profile |
| GET | `/candidate-profile/` | View candidate profile |
| PUT | `/candidate-profile/` | Update candidate profile |
| PATCH | `/candidate-profile/` | Partially update profile |

### Job Applications

| Method | Endpoint | Description |
|---|---|---|
| POST | `/jobs/<id>/apply/` | Apply for a job |
| GET | `/applications/` | View candidate applications |
| GET | `/applications/<id>/` | View application details |
| PATCH | `/applications/<id>/status` | Update application status (Recruiter) |

## Authentication

This project uses **Token Authentication** provided by Django REST Framework.

After successful registration or login, the API returns an authentication token.

For protected API requests, include the token in the request headers:

```http
Authorization: Token your_token_here
```

## User Roles and Permissions

| Feature | Recruiter | Candidate |
|---|---|---|
| Register / Login | Yes | Yes |
| View jobs | Yes | Yes |
| Create jobs | Yes | No |
| Update own jobs | Yes | No |
| Delete own jobs | Yes | No |
| Manage candidate profile | No | Yes |
| Apply for jobs | No | Yes |
| View own applications | No | Yes |
| Update application status | Own job applications | No |

## Database Models

The project contains four main models:

1. **User** – Custom user model with Recruiter and Candidate roles.
2. **Candidate** – Stores candidate information, qualifications, skills, and experience.
3. **Job** – Stores job details, salary range, location, experience, and recruiter information.
4. **Application** – Stores job application details and application status.

## API Testing

You can test the API endpoints using:

- Postman
- Thunder Client
- cURL

Make sure to provide the authentication token when accessing protected endpoints.

## Django Admin

Access the Django administration panel at:

`http://127.0.0.1:8000/admin/`

Login using your superuser credentials.

## Future Improvements

- Job search and filtering.
- Pagination.
- Email notifications.
- Resume upload.
- API documentation using Swagger.
- Automated API testing.

