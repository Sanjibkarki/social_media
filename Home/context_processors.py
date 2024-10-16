from django.shortcuts import render,HttpResponse
from django.views import View
from django.db.models.signals import post_save
from accounts.models import User
from .models import Profile,ChatModel,ReceiverModel,SenderModel
from django.shortcuts import redirect
from Post.models import PostX
import json
def name(request):
    if request.user.is_authenticated:
        followed_by = request.user.profile.followed_by.all().values()
        following = request.user.profile.follows.all().values()
        receiver = ReceiverModel.objects.get(user=request.user)
        senders = ChatModel.objects.filter(
    receiver= receiver,
    is_read=False
    ).values('sender').distinct()
        count = senders.count()
        context = {
            "user": request.user,
            "followed_by":len(followed_by)-1,
            "following":len(following)-1,
            "senderId": Profile.objects.get(user=request.user).id,
            "count": count
        }
        return context
    else:
        context = {
        "followed_by": 0,
        "following": 0
            
        }
        return context