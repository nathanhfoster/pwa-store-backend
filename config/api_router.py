from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from pwa_store_backend.users.api.views import UserViewSet, FavoritePwaViewSet
from pwa_store_backend.organizations.api.views import OrganizationViewSet
from pwa_store_backend.pwas.api.views.views import PwaViewSet, TagViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register('favorites', FavoritePwaViewSet)
router.register("organizations", OrganizationViewSet)
router.register("tags", TagViewSet)

router.urls

app_name = "api"
urlpatterns = router.urls + [
  path('', include("pwa_store_backend.pwas.api.urls")),
  path('auth/', include("pwa_store_backend.users.api.urls")),
]
