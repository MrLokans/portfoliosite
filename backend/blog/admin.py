from django.contrib import admin

from blog.forms import PostForm
from blog.models import Post


@admin.register(Post)
class FooModelAdmin(admin.ModelAdmin):
    form = PostForm
