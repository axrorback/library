from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1","localhost","library.coderboys.dev",]

CSRF_TRUSTED_ORIGINS = [
    "https://library.coderboys.dev",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'accounts',
    'analytics',
    'billing',
    'downloads',
    'library',
    'notification',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'django_ckeditor_5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

SITE_ID = 1

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
AWS_S3_CUSTOM_DOMAIN = 'media.axror.tech'
AWS_S3_FILE_OVERWRITE = False
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_SECRET'),
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'METHOD': 'oauth2',
        'VERIFIED_EMAIL': True,
    },
    'github': {
        'APP': {
            'client_id': os.getenv('GITHUB_CLIENT_ID'),
            'secret': os.getenv('GITHUB_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'user',
            'read:user',
            'user:email',
        ],
    }
}
SOCIALACCOUNT_LOGIN_ON_GET = True


CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_USER_MODEL = 'accounts.CustomUser'
SOCIALACCOUNT_ADAPTER = 'accounts.adapters.MySocialAccountAdapter'
ACCOUNT_ADAPTER = 'accounts.adapters.MyAccountAdapter'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

LOGOUT_REDIRECT_URL = 'login'

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BREVO_API_KEY = os.getenv('BREVO_API_KEY')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')



CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading", "|",
            "bold", "italic", "link", "|",
            "codeBlock", "|",

            "bulletedList", "numberedList", "|",
            "blockQuote", "insertTable", "|",
            "imageUpload", "|",
            "undo", "redo",
        ],

        "image": {
            "toolbar": [
                "imageTextAlternative",
                "toggleImageCaption",
                "linkImage",
            ]
        },

        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
            ]
        },

        "codeBlock": {
            "languages": [
                {"language": "plaintext", "label": "Plain text"},
                {"language": "python", "label": "Python"},
                {"language": "javascript", "label": "JavaScript"},
                {"language": "html", "label": "HTML"},
                {"language": "css", "label": "CSS"},
                {"language": "bash", "label": "Bash"},
                {"language": "json", "label": "JSON"},
                {"language": "sql", "label": "SQL"},
            ]
        },
    }
}