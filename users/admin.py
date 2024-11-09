from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]

    list_filter = ["is_staff", "is_active", "date_joined", "date_of_birth"]

    fieldsets = [
        (None, {"fields": ["email", "username", "avatar", "password"]}),
        (
            "Personal info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "patronymic",
                    "course",
                    "major",
                    "bio",
                    "telegram",
                    "vkontakte",
                ]
            },
        ),
        ("Stats", {"fields": ["points", "awards"]}),
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
                    "first_name",
                    "last_name",
                    "patronymic",
                    "course",
                    "major",
                    "avatar",
                    "date_of_birth",
                    "bio",
                    "is_staff",
                ],
            },
        ),
    ]

    search_fields = [
        "email",
        "username",
        "first_name",
        "last_name",
        "patronymic",
        "course",
        "major",
    ]

    ordering = [
        "email",
    ]

    filter_horizontal = []


admin.site.register(User, UserAdmin)
