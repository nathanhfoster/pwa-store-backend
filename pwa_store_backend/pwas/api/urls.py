from django.urls import path

from pwa_store_backend.pwas.api.extra_views import StoreInfoView

app_name = "pwas"
urlpatterns = [
    path("store-info", view=StoreInfoView.as_view(), name="store_info"),
]
