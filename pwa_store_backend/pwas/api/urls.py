from django.urls import path

from pwa_store_backend.pwas.api.extra_views import PwaInfoView

app_name = "pwas"
urlpatterns = [
    path("info", view=PwaInfoView.as_view(), name="info"),
]
