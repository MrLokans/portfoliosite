from rest_framework import serializers

from blog.models import Post


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


class PostCreateSerializer(serializers.ModelSerializer):

    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'created', 'author', 'title', 'content')
        read_only_fields = ('id', )
