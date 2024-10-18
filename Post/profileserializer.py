from rest_framework import serializers
from Home.models import User

class ProfileSerializer(serializers.Serializer):
    profileUsername = serializers.CharField(source='username', read_only=True)
    class Meta:
        model = User
        fields = ['profileUsername']