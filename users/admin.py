from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminDefault
from django.contrib.auth.forms import UserChangeForm as UserChangeFormDefault
from django.contrib.auth.forms import UserCreationForm as UserCreationFormDefault
# from users.forms import CustomUserChangeForm, CustomUserCreationForm
from users.models import User


class UserCreationForm(UserCreationFormDefault):
    class Meta:
        model = User
        fields = '__all__'


class UserChangeForm(UserChangeFormDefault):
    class Meta:
        model = User
        fields = '__all__'


class UserAdmin(UserAdminDefault):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'date_joined'
    )
    list_filter = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'date_joined'
    )
    fieldsets = (
        (None, {"fields": (
            "first_name",
            "last_name",
            "email",
            "password")}
         ),
        ("Permissions", {"fields": (
            "is_staff",
            "is_active",
            "groups",
            "user_permissions")}
         ),
    )
    add_fieldsets = (
        (None, {"fields": (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "date_of_birth",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions")}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, UserAdmin)
