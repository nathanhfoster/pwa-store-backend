from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'opt_in',
        'is_superuser', 'is_staff',
        'is_active', 'date_joined', 'last_login',)
    list_display_links = ('id', 'username', 'email',)
    search_fields = ('id', 'username', 'email', )


admin.site.register(User, UserAdmin)
