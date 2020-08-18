from django import forms

from articles.models import Comment


class CommentForm(forms.ModelForm):
    required_css_class = "required"
    error_css_class = "error"

    class Meta:
        model = Comment
        fields = ["username", "email", "content"]
