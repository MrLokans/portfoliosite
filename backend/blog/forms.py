from django import forms

from pagedown.widgets import AdminPagedownWidget

from blog.models import Post


class PostForm(forms.ModelForm):

    content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Post
        fields = "__all__"