# Phoenix Blogs Settings

import os
from pathlib import Path
from dotenv import load_dotenv
from django.urls import reverse_lazy


BASE_DIR = Path(__file__).resolve().parent.parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

SECRET_KEY    = os.getenv('SECRET_KEY')
DEBUG         = bool(os.getenv('DEBUG'))
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS",'').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'blog',
    'rest_framework',
    # 'rest_framework_simplejwt',
    'corsheaders',
    'hashids',
    'ckeditor',
    'ckeditor_uploader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = bool(os.getenv("CORS_ORIGIN_ALLOW_ALL"))

CORS_ORIGIN_WHITELIST = os.getenv("CORS_ORIGIN_WHITELIST",'').split(',')


# Url Settings
ROOT_URLCONF        = 'blog_app.urls'
LOGIN_REDIRECT_URL  = reverse_lazy('blog:dashboard')
LOGOUT_REDIRECT_URL = reverse_lazy('blog:index_blogs')


# Template Settings
TEMPLATES = [
    {
        'BACKEND'  : 'django.template.backends.django.DjangoTemplates',
        'DIRS'     : [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS' : True,
        'OPTIONS'  : {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'blog_app.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.postgresql',
        'NAME'     : os.getenv('DB_NAME'),
        'USER'     : os.getenv('DB_USER'),
        'PASSWORD' : os.getenv('DB_PASSWORD'),
        'HOST'     : os.getenv('DB_HOST'),
        'PORT'     : int(os.getenv('DB_PORT')),
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


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

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     )
# }


LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True 
USE_TZ        = True


# Static configuration
STATIC_URL       = '/static/'
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'static'),
)
STATIC_ROOT      = os.path.join(CORE_DIR, 'staticfiles')


# Media configuration
MEDIA_URL   = '/media/'
MEDIA_ROOT  = os.path.join(CORE_DIR, 'media/')



# CKEditor Configuration
CKEDITOR_UPLOAD_PATH          = "uploads/ck_editor/"
CKEDITOR_MEDIA_PREFIX         = "/media/ckeditor"
CKEDITOR_IMAGE_BACKEND        = "pillow"
CKEDITOR_RESTRICT_BY_USER     = False
CKEDITOR_REQUIRE_STAFF        = False
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar'               : 'full',
        'uploadUrl'             : '/ckeditor/upload/',
        'filebrowserUploadUrl'  : '/ckeditor/upload/',
        'imageUploadUrl'        : '/ckeditor/upload/',
        'startupFocus'          : True,
        'height'                : 300,
        'width'                 : "100%",
    },
}
