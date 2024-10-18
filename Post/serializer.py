from rest_framework import serializers
from Home.models import ChatModel
from .models import PostX
from .profileserializer import ProfileSerializer
class chatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = '__all__'


class Myserializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    hasLiked = serializers.SerializerMethodField()
    totalLikes = serializers.SerializerMethodField()
    
    class Meta:
        model = PostX
        fields = [
            'id',
            'caption',
            'image',
            'date_of_post',
            'hasLiked',
            'totalLikes',
            'profile'
        ]
        
    def get_hasLiked(self, obj):
        request = self.context.get('request')
        if request.user in obj.liked_by.all():
            return True
        else:
            return False

    def get_totalLikes(self, obj):
        return obj.liked_by.count()
