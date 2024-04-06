from django.db import models
from accounts.models import User
# Create your models here.

class PostX(models.Model):
    profile = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    caption = models.CharField(max_length = 400)
    date_of_post = models.DateTimeField(auto_now_add = True)
    
    @property
    def user_has_liked(self,user):
        return self.likes.filter(profile=user).exists()
class Likes(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostX,related_name="likes", on_delete=models.CASCADE)
    liked = models.BooleanField(default = False)
    Liked_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('profile', 'post')

    def __str__(self):
        return f"{self.profile.username} likes {self.post.caption[:50]}"