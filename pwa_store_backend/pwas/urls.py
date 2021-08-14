from django.urls import path, include
from .api.views import PwaViewSet, TagViewSet, RatingViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('pwas', PwaViewSet)
router.register('tags', TagViewSet)
router.register('ratings', RatingViewSet)


app_name = "pwas"

urlpatterns = [
    path('', include(router.urls))
]