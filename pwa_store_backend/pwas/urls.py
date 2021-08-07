from django.urls import path, include
from .views import PwaView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('organizations', PwaView)

urlpatterns = [
    path('', include(router.urls))
]