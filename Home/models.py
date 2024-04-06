from django.db import models
from accounts.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    follows = models.ManyToManyField(

        "self",

        related_name="followed_by",

        symmetrical=False,

        blank=True

    )
    
    def __str__(self):
        return self.user.username
    