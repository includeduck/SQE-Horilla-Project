"""Production URLs plus test-only static serving for a disposable live server."""

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = staticfiles_urlpatterns() + [path("", include("horilla.urls"))]
