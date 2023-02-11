"""Define forms for posts app."""
from django import forms

from posts.models import Post, Comment


class PostForm(forms.ModelForm):
    """Process posting new posts."""

    class Meta:
        """PostForm Meta."""

        model = Post
        fields = ("text", "group", "image")


class CommentForm(forms.ModelForm):
    """Process commenting."""

    class Meta:
        """CommentForm Meta."""

        model = Comment
        fields = ("text",)
