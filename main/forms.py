from django import forms
from django_select2 import forms as s2forms
from django.forms import modelformset_factory

from django.contrib.auth import get_user_model
from registry.models import Major, University
from .models import Post, Comment, Media, Profile
from django.contrib.contenttypes.admin import GenericStackedInline


User = get_user_model()


class UniversityWidget(s2forms.ModelSelect2Widget):
    queryset = University.objects.all().order_by("name")
    is_required = False
    search_fields = [
        "name__icontains",
        "city__icontains",
        "country__icontains",
    ]


class MajorWidget(s2forms.ModelSelect2Widget):
    queryset = Major.objects.all().order_by("name")
    is_required = False
    search_fields = [
        "name__icontains",
    ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        widgets = {
            "university": UniversityWidget,
            "major": MajorWidget,
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class PostForm(forms.ModelForm):
    media_files = MultipleFileField(required=False)

    class Meta:
        model = Post
        fields = ["title", "content", "category", "tags"]


class EditProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    avatar = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control-file"})
    )

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
    )

    autocomplete_fields = ["university", "major"]

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "middle_name",
            "university",
            "major",
            "date_of_birth",
            "bio",
            "avatar",
            "telegram",
            "vkontakte",
        ]
        widgets = {
            "university": UniversityWidget,
            "major": MajorWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update(
            {"placeholder": "Ivan", }
        )

        self.fields["last_name"].widget.attrs.update(
            {"placeholder": "Ivanov", }
        )

        self.fields["middle_name"].widget.attrs.update(
            {"placeholder": "Ivanovich", }
        )

        self.fields["telegram"].widget.attrs.update(
            {"placeholder": "https://t.me/username", }
        )

        self.fields["vkontakte"].widget.attrs.update(
            {"placeholder": "https://vk.com/username", }
        )

        self.fields["bio"].widget.attrs.update(
            {"placeholder": "Write something about yourself", }
        )
        
