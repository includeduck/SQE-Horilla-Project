"""Production routes and an explicitly test-only scoped schema fallback."""
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from area2_urls import urlpatterns as production_patterns
scoped = get_schema_view(
    openapi.Info(title="Isolated Area 2 leave schema", default_version="v1"),
    patterns=[path("api/v1/leave/", include("horilla_api.api_urls.leave.urls"))],
    public=True, permission_classes=(AllowAny,),
)
urlpatterns = production_patterns + [
    path("__area2_contract_schema__/", scoped.without_ui(cache_timeout=0)),
]
