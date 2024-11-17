from .models import User
from django import forms
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    SetPasswordForm,
)
from django.contrib.auth import password_validation
from random_username.generate import generate_username
from django.contrib.auth.password_validation import validate_password


class UserCreationForm(forms.ModelForm):
    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control"},
        ),
        required=True,
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password],
        min_length=8,
        max_length=50,
        help_text=password_validation.password_validators_help_text_html(),
        required=True,
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        min_length=8,
        max_length=50,
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean(self):
        _ = super(UserCreationForm, self).clean()
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                self.add_error(
                    "password2",
                    "Passwords don't match. Please enter both fields again.",
                )
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = generate_username()[0]
        user.is_active = False
        if commit:
            user.save()
        return user


class UserSetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"
