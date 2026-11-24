"""Settings for Area 1 white-box unit tests.

In-memory SQLite, built from the models without running migrations (fast and
isolated: never touches TestDB.sqlite3 or Rayyan's Area 2 databases).
"""

import os

os.environ["DEBUG"] = "True"
os.environ["HORILLA_ENV"] = "test"
os.environ.setdefault("SECRET_KEY", "sqe-unit-synthetic-test-key-not-for-production")

from horilla.settings import *  # noqa: E402,F403

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
TIME_ZONE = "Asia/Karachi"
