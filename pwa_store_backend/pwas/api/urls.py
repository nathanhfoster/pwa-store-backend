from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from pwa_store_backend.pwas.api.views.extra_views import PwaInfoView
from .views.views import PwaViewSet
from .views.rating_views import RatingViewSet

app_name = "pwas"

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('pwas', PwaViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = router.urls + [
    path("info", view=PwaInfoView.as_view(), name="info"),
]
