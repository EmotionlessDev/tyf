from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def email_clean(self):
        email = self.cleaned_data["email"].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email already exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"


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
