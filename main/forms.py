from django import forms
from django_select2 import forms as s2forms
from django.forms import modelformset_factory

from registry.models import Major, University
from .models import Post, Comment, Media, Profile
from django.contrib.contenttypes.admin import GenericStackedInline


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


class CommentForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=Comment.objects.all(),
        widget=forms.HiddenInput,
        required=False
    )

    class Meta:
        model = Comment
        fields = ("content", "parent", )
        labels = {
            "content": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs.update(
            {"class": "form-control comments__content", "placeholder": "..."}
        )
