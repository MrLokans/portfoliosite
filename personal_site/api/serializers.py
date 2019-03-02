from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        User = get_user_model()

        user = User.objects.create(username=validated_data["username"])

        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ("username", "password")
