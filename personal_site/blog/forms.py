from django import forms

from .models import Post


class FlatPageForm(forms.ModelForm):
    post_title = forms.CharField(label='You name', max_length=100)
    content = forms.CharField()

    class Meta:
        model = Post
        fields = ()
