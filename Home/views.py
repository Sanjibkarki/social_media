from django.shortcuts import render,HttpResponse
from django.views import View
from django.db.models.signals import post_save
from accounts.models import User
from .models import Profile,SenderModel,ReceiverModel,ChatModel,ChatKeyModel
from django.shortcuts import redirect
from Post.models import PostX
from django.views.generic import ListView
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.
class Index(ListView):
    def get(self,request):
        post = PostX.objects.all()
        if post:
            return render(request,'front_pages/main_page.html')
        else:
            return render(request,'front_pages/no_page.html')
    
class Follow(View):
    def get(self,request):
        following =request.user.profile.follows.all().values_list('user_id')
        profile = Profile.objects.exclude(user = request.user)
        context = {
            "profile" : profile,
            "following":following
        }
        return render(request,"front_pages/follow.html",context)

class follow_activity(View):
    def get(self,request):
        pass
    
def Followx(request,id):
    try:
        follow = Profile.objects.get(id = id)        
        if request.POST.get('status') == "unfollow":
            remove = request.user.profile.follows.remove(follow)
        elif request.POST.get('status') == "follow":
            add = request.user.profile.follows.add(follow)
    except Profile.DoesNotExist:
        follow = None
    return redirect("follow")

class Add_New_Post(View):
    def get(self,request):
        return render(request,'front_pages/add_post.html')
    
    def post(self,request):
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        post = PostX(profile = request.user,image = image,caption= caption)
        post.save()
        return redirect('add_post')

class Info(View):
    def get(self,request):
        profile = Profile.objects.get(user = request.user)
        user = User.objects.get(email = request.user)
        user_posts = user.postx_set.all()
        return render(request,"front_pages/profile.html",{"profile":profile,'user_posts':user_posts})
 
class Message(View):
    def get(self,request):
        friend = request.user.profile.follows.exclude(user=request.user).all()
        user = SenderModel.objects.get(user = request.user)
        return render(request,"front_pages/messages.html",{"friend":friend}) 
    
class Room(View):
    def get(self,request,user_id):
        user1 = User.objects.get(pk=request.user.pk)        
        receiver = Profile.objects.get(pk=user_id).user
        #receiver
        user2 = User.objects.get(email=receiver)

        # Setup sender and receiver models
        user1_sender = SenderModel.objects.get(user=user1.sendermodel.user)
        user2_sender = SenderModel.objects.get(user=user2.sendermodel.user)
        user1_receiver = ReceiverModel.objects.get(user=user1.receivermodel.user)
        user2_receiver = ReceiverModel.objects.get(user=user2.receivermodel.user)

        # Get the sender and receiver chats to each other
        user1_chats = ChatModel.objects.filter(sender=user1_sender, receiver=user2_receiver)
        user2_chats = ChatModel.objects.filter(sender=user2_sender, receiver=user1_receiver)
        
        # Put the chats in to `chats` list
        chats = [chat1 for chat1 in user1_chats]
        if not user1.get_username() == user2.get_username():
            
            chats.extend([chat2 for chat2 in user2_chats])
            chats.sort(key=self.sort_pk)

        # Add the chats and user2 to context
        # for passing to template
        context = {
            'chats': chats,
            'user2': user2,
            'userId':user_id
        }
        return render(request,"front_pages/room.html",context)
    
    def sort_pk(self, model):
        return model.pk
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()




@receiver(post_save , sender=User)
def new_user(sender , instance , created , **kwargs):
    if created:
        # Create SenderModel and ReceiverModel for new User instance
        SenderModel.objects.create(user=instance)
        ReceiverModel.objects.create(user=instance)

        # Create a ChatKeyModel for each user on all users with the new user.
        # Even the new user itself will have its own ChatKeyModel
        users = User.objects.all()
        for user in users:
            user_username = user.get_username()
            new_user_username = instance.get_username()
            usernames = [user_username]
            if not user_username == new_user_username:
                # If not the user username is equal to the new instance username
                # add the username
                # This is to avoid two same username 
                usernames.append(new_user_username)
            ChatKeyModel.objects.create(
                usernames=usernames
            )

from django.core.cache import cache
    
@receiver(post_save, sender=ChatModel)
def notify_user(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    profile = Profile.objects.get(user = instance.sender.user).id
    async_to_sync(channel_layer.group_send)(
        f'user_{Profile.objects.get(user = instance.receiver.user).id}',
        {
            'type': 'send.notification',
            'sender': profile,
            'message': f'New message from {instance.sender.user.email}',     
        }
    )