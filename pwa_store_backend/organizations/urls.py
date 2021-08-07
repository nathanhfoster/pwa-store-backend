from django.urls import path, include
from .views import OrganizationView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('organizations', OrganizationView)

urlpatterns = [
    path('', include(router.urls))
]