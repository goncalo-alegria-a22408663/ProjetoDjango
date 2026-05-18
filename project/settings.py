"""
Django settings for project.
"""

from pathlib import Path
import os
import environ


BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
}

# Environment variables
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "django-insecure-local-development-key"),
    ALLOWED_HOSTS=(list, ["127.0.0.1", "localhost"]),
    CSRF_TRUSTED_ORIGINS=(list, []),
    EMAIL_BACKEND=(str, "django.core.mail.backends.console.EmailBackend"),
    EMAIL_HOST=(str, "smtp.gmail.com"),
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
)

environ.Env.read_env(BASE_DIR / ".env")


# Security
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "portfolio",
    "escola",
    "accounts",
    "artigos",
    "markdownify.apps.MarkdownifyConfig",
    "cloudinary",
    "cloudinary_storage",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.is_gestor_portfolio",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
DATABASES = {
    "default": env.db("DATABASE_URL")
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "pt-pt"
TIME_ZONE = "Europe/Lisbon"
USE_I18N = True
USE_TZ = True


# Static files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"





# Markdownify
MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            "a",
            "abbr",
            "acronym",
            "strong",
            "b",
            "blockquote",
            "em",
            "i",
            "ul",
            "li",
            "ol",
            "p",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "code",
            "pre",
            "hr",
            "br",
            "table",
            "thead",
            "tbody",
            "tr",
            "th",
            "td",
        ],
        "MARKDOWN_EXTENSIONS": [
            "markdown.extensions.fenced_code",
            "markdown.extensions.tables",
        ],
    }
}


# Authentication redirects
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "/portfolio/projetos/"
LOGOUT_REDIRECT_URL = "/portfolio/projetos/"


# Email
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")


# Proxy settings for deployment
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media files
MEDIA_URL = "/media/"


STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}