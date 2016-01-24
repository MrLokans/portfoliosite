from django import forms

from .models import Post
from tinymce.widgets import TinyMCE


class FlatPageForm(forms.ModelForm):
    post_title = forms.CharField(label='You name', max_length=100)
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Post
        fields = ()
