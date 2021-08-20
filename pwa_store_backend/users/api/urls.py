from django.urls import path
from .views import LoginView, RegisterView, UpdateSettingsView

app_name = "users"
urlpatterns = [
    path("login", LoginView.as_view(), name="api_login"),
    path("register", RegisterView.as_view(), name="api_register"),
    path("update-settings/<int:pk>", UpdateSettingsView.as_view(), name="update_settings"),
]
