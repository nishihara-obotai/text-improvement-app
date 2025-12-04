import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# django-environの設定
env = environ.Env(
    # デフォルト値を設定
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, []),
)

# .envファイルを読み込む
environ.Env.read_env(BASE_DIR / ".env")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Site Settings
# サイト名（全テンプレートから{{ SITE_NAME }}で参照可能）
SITE_NAME = "文章改善ツール"  # ← ここを変更してアプリ名をカスタマイズ

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # WhiteNoiseを使用（staticfilesの前に配置）
    "django.contrib.staticfiles",
    "import_export",  # データインポート・エクスポート
    "textapp",  # 文章改善アプリ
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoiseミドルウェア（SecurityMiddlewareの直後）
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # プロジェクト直下のtemplatesフォルダ
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.site_settings",  # サイト設定を全テンプレートで利用可能に
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# デフォルトはSQLite3、環境変数DATABASE_URLで上書き可能（PostgreSQL等）
DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}

# Google Cloud Platform (GCP) Credentials
# Gemini (Vertex AI)やGCPの各種サービスを使用する場合のクレデンシャル設定
# .envから読み取り、環境変数が未設定の場合は上書き（GoogleのPythonパッケージが環境変数を利用するため）
GOOGLE_APPLICATION_CREDENTIALS = env("GOOGLE_APPLICATION_CREDENTIALS", default=None)
if (
    GOOGLE_APPLICATION_CREDENTIALS
    and "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ
):
    # 相対パスの場合は絶対パスに変換
    credentials_path = Path(GOOGLE_APPLICATION_CREDENTIALS)
    if not credentials_path.is_absolute():
        credentials_path = BASE_DIR / credentials_path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)

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
LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # collectstaticで集める先
STATICFILES_DIRS = [
    BASE_DIR / "assets",  # assetsフォルダから静的ファイルを収集
]

# WhiteNoiseの設定
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login settings
LOGIN_URL = "/app/login/"
LOGIN_REDIRECT_URL = "/app/"
LOGOUT_REDIRECT_URL = "/app/login/"
