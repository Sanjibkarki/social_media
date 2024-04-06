from django.shortcuts import render,HttpResponse
from django.views import View
from django.db.models.signals import post_save
from accounts.models import User
from .models import Profile
from django.shortcuts import redirect
from Post.models import PostX,Likes
from django.views.generic import ListView

# Create your views here.
class Index(ListView):
    model = PostX
    
    def get_queryset(self):
        request = self.request 
        try:  
            following_post=request.user.profile.follows.all().values_list('user')
            queryset = PostX.objects.filter(profile__in = following_post)
        except PostX.DoesNotExist:
            queryset = None
        return queryset
    
    def get(self,request):
        queryset = self.get_queryset()
        if not queryset.exists():
            return render(request,'front_pages/no_post.html')

        else:
            return render(request,'front_pages/main_page.html',{"object_list":queryset})
    
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
 
       
def create_profile(sender, instance, created, **kwargs):
    
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()

post_save.connect(create_profile, sender=User)