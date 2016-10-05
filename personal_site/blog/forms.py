from django import forms

from markdownx.fields import MarkdownxFormField

from .models import Post


class FlatPageForm(forms.ModelForm):
    post_title = forms.CharField(label='You name', max_length=100)
    content = MarkdownxFormField()

    class Meta:
        model = Post
        fields = ()
