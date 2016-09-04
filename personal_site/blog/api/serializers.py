from blog.models import Post

from rest_framework import serializers


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'content',
            'created',
        ]
