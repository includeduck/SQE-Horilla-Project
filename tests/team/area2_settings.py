"""Disposable Area 2 database/media; never uses or resets the user's local DB."""

import atexit
import os
import shutil
import tempfile
from pathlib import Path

os.environ["DEBUG"] = "True"
os.environ["HORILLA_ENV"] = "test"
os.environ.setdefault("SECRET_KEY", "sqe-area2-synthetic-test-key-do-not-use-in-production")

from horilla.settings import *  # noqa: E402,F403

AREA2_TEMP_ROOT = Path(tempfile.mkdtemp(prefix="sqe-area2-"))
AREA2_ISOLATED_TESTS = True
atexit.register(shutil.rmtree, AREA2_TEMP_ROOT, ignore_errors=True)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(AREA2_TEMP_ROOT / "bootstrap.sqlite3"),
        "TEST": {"NAME": str(AREA2_TEMP_ROOT / "test.sqlite3")},
        "OPTIONS": {"timeout": 30},
    }
}
MEDIA_ROOT = str(AREA2_TEMP_ROOT / "media")
STORAGES = {**STORAGES, "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"}}  # noqa: F405
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
# These accounts are disposable synthetic fixtures. Use Django's fast test
# hasher while retaining real password verification and JWT issuance over HTTP.
# Production password configuration and password-security evaluation are unchanged.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]
CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://127.0.0.1"]
SECURE_SSL_REDIRECT = False
TIME_ZONE = "Asia/Karachi"
