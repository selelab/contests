from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from contests.urls import router as contests_router
from . import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Selelab Contests API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)


class RouterExtendable(routers.DefaultRouter):
    """
    Extends `DefaultRouter` class to add a method for extending url routes from another router.
    """
    def extend(self, router):
        """
        Extend the routes with url routes of the passed in router.

        Args:
             router: SimpleRouter instance containing route definitions.
        """
        self.registry.extend(router.registry)


api_router = RouterExtendable()
api_router.extend(contests_router)

urlpatterns = [
    url(r'^jwt-token/', obtain_jwt_token),
    url(r'^jwt-token/verify/', verify_jwt_token),
    url(r'^jwt-token/refresh/', refresh_jwt_token),
    url(r'^$', RedirectView.as_view(url='./swagger/')),
    url(r'^swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^admin/', admin.site.urls),
    url(r'^v1/', include(api_router.urls)),
]
