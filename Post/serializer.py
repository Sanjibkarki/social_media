from rest_framework import serializers
from Home.models import ChatModel
from .models import Likes,PostX
class chatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = '__all__'

class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['profile','post','liked','Liked_at']

class Myserializer(serializers.ModelSerializer):
    class Meta:
        model = PostX
        fields = ['profile']
