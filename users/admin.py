from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        "email",
        "is_staff",
        "is_active",
    ]

    list_filter = ["is_staff", "is_active", "date_joined"]

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_active", "is_staff"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                ],
            },
        ),
    ]

    search_fields = [
        "email",
    ]

    ordering = [
        "email",
    ]

    filter_horizontal = []


admin.site.register(User, UserAdmin)
