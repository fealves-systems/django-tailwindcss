import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from django.core.signals import setting_changed
from django.dispatch import receiver
from pprint import pformat

# Load environment variables from a .env file
load_dotenv()

AUTH_USER_MODEL = 'accounts.CustomUser'
# Construindo caminhos dentro do projeto usando Path.
BASE_DIR = Path(__file__).resolve().parent.parent

# Nome do projeto
PROJECT_NAME = os.environ.get('DJANGO_ENV', 'project')

# AVISO DE SEGURANÇA: mantenha a chave secreta usada em produção como secreta!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 'default-secret-key-please-change-me'
)

# Determinando o ambiente de execução
ENVIRONMENT = os.environ.get('DJANGO_ENV', 'dev')

# AVISO DE SEGURANÇA: não execute com debug ligado em produção!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') != 'False'

# Diretório base para logging
LOGGING_DIR = BASE_DIR / 'logs' / os.environ.get('LOGGING_DIR', ENVIRONMENT)

# Hosts permitidos
ALLOWED_HOSTS = os.environ.get(
    'DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1'
).split(',')

# Origens confiáveis para CSRF
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'DJANGO_CSRF_TRUSTED_ORIGINS',
    'http://localhost,https://localhost,http://127.0.0.1,https://127.0.0.1',
).split(',')

from pathlib import Path
from django.core.signals import setting_changed


def ensure_directory_exists(path):
    """
    Garante que o diretório especificado exista. Se não existir, cria o diretório.

    Args:
    path (str or pathlib.Path): O caminho do diretório a ser verificado e possivelmente criado.
    """
    directory = Path(path)
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
        print(f'O diretório {directory} foi criado.')
    else:
        print(f'O diretório {directory} já existe.')


# Flag para garantir que a função seja executada apenas uma vez
_settings_printed = False


from pprint import pformat




# Definição de aplicações
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = ['accounts']

THIRDY_PARTY_APPS = ['compressor']

INSTALLED_APPS += PROJECT_APPS + THIRDY_PARTY_APPS


COMPRESS_ROOT = BASE_DIR / 'static'

COMPRESS_ENABLED = True

STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = f'{PROJECT_NAME}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = f'{PROJECT_NAME}.wsgi.application'

# Configuração de banco de dados
if ENVIRONMENT == 'dev':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DATABASE_NAME', 'postgres'),
            'USER': os.environ.get('DATABASE_USER', 'postgres'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
            'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
            'PORT': os.environ.get('DATABASE_PORT', '5432'),
        }
    }

# Configuração de validação de senhas
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

ensure_directory_exists(LOGGING_DIR)

# Configuração de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOGGING_DIR
            / f'{PROJECT_NAME}_log_{datetime.now().strftime("%Y%m%d")}.txt',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,  # Mantém logs dos últimos 7 dias
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {  # logger raiz
            'handlers': ['console', 'file']
            if ENVIRONMENT == 'dev'
            else ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Internacionalização
LANGUAGE_CODE = os.environ.get('DJANGO_LANGUAGE_CODE', 'en-us')
TIME_ZONE = os.environ.get('DJANGO_TIME_ZONE', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Arquivos estáticos (CSS, JavaScript, Imagens)
STATIC_URL = '/static/'
# Ou, se estiver usando uma CDN:
# STATIC_URL = 'https://cdn.example.com/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Tipo de chave primária padrão
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Used for custom user accounts
# AUTH_USER_MODEL = 'accounts.UserAccount'

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER','')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
# EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False') == 'False'

LOGOUT_REDIRECT_URL = 'login'


def print_settings_summary():
    """
    Função para imprimir um resumo das configurações se DEBUG = True.
    """
    global _settings_printed
    if not _settings_printed:
        if DEBUG:
            settings_summary = {
                'BASE_DIR': str(BASE_DIR),
                'PROJECT_NAME': PROJECT_NAME,
                'ENVIRONMENT': ENVIRONMENT,
                'DEBUG': DEBUG,
                'LOGGING_DIR': str(LOGGING_DIR),
                'ALLOWED_HOSTS': ALLOWED_HOSTS,
                'CSRF_TRUSTED_ORIGINS': CSRF_TRUSTED_ORIGINS,
                'INSTALLED_APPS': INSTALLED_APPS,
                'MIDDLEWARE': MIDDLEWARE,
                'DATABASES': DATABASES,
                'LANGUAGE_CODE': LANGUAGE_CODE,
                'TIME_ZONE': TIME_ZONE,
                'USE_I18N': USE_I18N,
                'USE_L10N': USE_L10N,
                'USE_TZ': USE_TZ,
                'STATIC_URL': STATIC_URL,
                'STATIC_ROOT': str(STATIC_ROOT),
                'STATICFILES_DIRS': [str(path) for path in STATICFILES_DIRS],
                'MEDIA_URL': MEDIA_URL,
                'MEDIA_ROOT': str(MEDIA_ROOT),
                'DEFAULT_AUTO_FIELD': DEFAULT_AUTO_FIELD,
                'EMAIL_BACKEND': EMAIL_BACKEND,
                'EMAIL_HOST': EMAIL_HOST,
                'EMAIL_PORT': EMAIL_PORT,
                'EMAIL_HOST_USER': EMAIL_HOST_USER,
                'EMAIL_USE_TLS': EMAIL_USE_TLS
            }
            formatted_settings = pformat(settings_summary, indent=2)
            print('Resumo das Configurações:')
            print(formatted_settings)
            
            _settings_printed = True
        else:
            print('DEBUG está desativado, o resumo das configurações não será impresso.')
    else:
        print('As configurações já foram impressas.')

# Atrelar a função ao início do sistema se DEBUG for True
if DEBUG:
    print_settings_summary()

# Alternativamente, você pode usar um signal para imprimir as configurações quando uma delas for alterada
@receiver(setting_changed)
def handle_setting_changed(sender, setting, value, **kwargs):
    global _settings_printed
    if setting == 'DEBUG' and value is True and not _settings_printed:
        print_settings_summary()
