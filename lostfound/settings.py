"""
Django settings for lostfound project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# SECURITY
# ---------------------------------------------------------
SECRET_KEY = "django-insecure-%5f7o(-nv3*c53#9z#6hydo*qv$q5jm%4x31551ckjgg^8gi!#"
DEBUG = True

ALLOWED_HOSTS = [
    "195.181.241.184",
    "lostatschool.space",
    "www.lostatschool.space",
]

# ---------------------------------------------------------
# APPLICATIONS
# ---------------------------------------------------------
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Allauth (required)
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    # Google
    "allauth.socialaccount.providers.google",

    # Your app
    "core.apps.CoreConfig",
]

SITE_ID = 1

# ---------------------------------------------------------
# AUTHENTICATION BACKENDS
# ---------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# ---------------------------------------------------------
# ALLAUTH (STABLE CONFIG — FIXES REDIRECT LOOP)
# ---------------------------------------------------------

ACCOUNT_AUTHENTICATION_METHOD = "username_email"  # allow both
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# Disable new API completely
ACCOUNT_LOGIN_METHODS = None
ACCOUNT_SIGNUP_FIELDS = None






# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # REQUIRED
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------------------------
# URL / WSGI
# ---------------------------------------------------------
ROOT_URLCONF = "lostfound.urls"
WSGI_APPLICATION = "lostfound.wsgi.application"

# ---------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "core" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",  # REQUIRED by allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------
# STATIC & MEDIA
# ---------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------
# CSRF SECURITY
# ---------------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    "https://lostatschool.space",
    "https://www.lostatschool.space",
]

# ---------------------------------------------------------
# ALLAUTH Google OAuth
# ---------------------------------------------------------
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "40209877876-pquvm9m0f87da3biiuu9j6dtlnu88i3i.apps.googleusercontent.com",
            "secret": "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",
            "key": "",
        }
    }
}

# ---------------------------------------------------------
# EMAIL
# ---------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "augustas.stancikas@gmail.com"

# ---------------------------------------------------------
# ERROR HANDLERS
# ---------------------------------------------------------
HANDLER404 = "core.views.custom_404"
HANDLER500 = "core.views.custom_500"
