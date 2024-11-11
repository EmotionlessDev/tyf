from django import forms
from django.forms import modelformset_factory

from .models import Post, Comment, Media


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "category"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ["file", "description"]


MediaFormSet = modelformset_factory(Media, form=MediaForm, extra=10)
