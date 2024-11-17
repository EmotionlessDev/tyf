from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from random_username.generate import generate_username

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

    # def save_model(self, request, obj, form, change):
    #     if obj.username is None:
    #         obj.username = generate_username()[0]
    #     if not obj.is_active:
    #         obj.is_active = True
    #     super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
