# Digital Library

Digital Library is a Django-based online library system for managing categories, books, user accounts, donations, paid book access, and notification workflows. The project includes authentication, social login, Telegram verification, email flows, payment callbacks, Celery tasks, and media storage support.

## Features

- User registration, login, logout, password reset, and profile management
- Google and GitHub social login via `django-allauth`
- Book and category browsing with detail pages
- Paid book access and book payment callbacks
- Donation page with quick amount selection
- Telegram verification and disconnect flows
- Email notifications for OTP and password reset
- Background tasks with Celery and Redis
- Static file serving with WhiteNoise
- Media storage support through S3-compatible storage

## Tech Stack

- Python 3
- Django 6
- PostgreSQL
- Redis
- Celery
- Gunicorn
- Nginx
- Bootstrap 5
- CKEditor 5

## Project Structure

- `accounts/` - authentication, profile, Telegram, and password flows
- `analytics/` - analytics-related models and views
- `billing/` - donations and payment handling
- `downloads/` - download-related logic
- `library/` - categories, books, book details, and book payments
- `notification/` - notification models and views
- `bot/` - Telegram bot code
- `config/` - project settings, URLs, ASGI/WSGI, Celery config
- `templates/` - shared and app-specific HTML templates

## Requirements

The main Python dependencies are listed in `requirements.txt`. Key packages include:

- `Django`
- `celery`
- `redis`
- `django-allauth`
- `django-ckeditor-5`
- `psycopg2-binary`
- `whitenoise`
- `django-storages`
- `boto3`
- `gunicorn`

## Environment Variables

Create a `.env` file in the project root with values similar to the following:

```env
SECRET_KEY=your-secret-key
DEBUG=True

EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-email-password

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_SECRET=your-google-secret

GITHUB_CLIENT_ID=your-github-client-id
GITHUB_SECRET=your-github-secret

AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_ENDPOINT_URL=your-s3-endpoint
```

If you use a PostgreSQL database in Docker, the `db` service will also read its credentials from `.env`.

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. Create a superuser:

```bash
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

## Docker Setup

The project includes a `docker-compose.yml` file with the following services:

- `db` - PostgreSQL 15
- `redis` - Redis cache/broker
- `web` - Django app served by Gunicorn
- `celery` - background worker
- `celery-beat` - scheduled tasks
- `nginx` - reverse proxy and static/media delivery

To start the stack:

```bash
docker compose up --build
```

## Useful Commands

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
celery -A config worker -l info
celery -A config beat -l info
```

## Main URLs

- `/` - category list / home
- `/accounts/` - authentication and profile routes
- `/payment/` - donation and payment callback routes
- `/ckeditor5/` - CKEditor integration
- `/admin/` - Django admin

## Notes

- The project currently uses SQLite in the default Django settings, while `docker-compose.yml` is prepared for PostgreSQL.
- Static files are served through WhiteNoise in the Django stack.
- Media files are configured for S3-compatible storage.
