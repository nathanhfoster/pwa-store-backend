from django.urls import path, include
from .views import PwaView, TagView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('pwas', PwaView)
router.register('tags', TagView)


app_name = "pwas"

urlpatterns = [
    path('', include(router.urls))
]