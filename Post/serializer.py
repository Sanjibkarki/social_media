from rest_framework import serializers
from .models import Likes,PostX
class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['profile','post','liked','Liked_at']

class Myserializer(serializers.ModelSerializer):
    class Meta:
        model = PostX
        fields = ['profile']
