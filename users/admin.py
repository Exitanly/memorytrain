from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'level', 'total_points', 'is_staff')
    list_filter = ('level', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Game Stats', {'fields': ('level', 'experience', 'total_points')}),
    )
    readonly_fields = ('level', 'experience', 'total_points')

admin.site.register(User, CustomUserAdmin)