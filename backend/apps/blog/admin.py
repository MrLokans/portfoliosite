from django.contrib import admin

from .forms import PostForm
from .models import Post


@admin.register(Post)
class FooModelAdmin(admin.ModelAdmin):
    form = PostForm
