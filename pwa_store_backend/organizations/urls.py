from django.urls import path, include
from .api.views import OrganizationView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('organizations', OrganizationView)

app_name = "organizations"

urlpatterns = [
    path('', include(router.urls))
]