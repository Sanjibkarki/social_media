from django.db import models
from accounts.models import User
# Create your models here.

class PostX(models.Model):
    profile = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    caption = models.CharField(max_length = 400)
    date_of_post = models.DateTimeField(auto_now_add = True)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True) 
    
    