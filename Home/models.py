from accounts.models import User
from uuid import uuid4

from django.db import models
from accounts.models import User
from django.utils.timezone import now
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



class SenderModel(models.Model):
    '''Model for the sender of chat'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.get_username()
    
class ReceiverModel(models.Model):
    '''Model for the receiver of chat'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.get_username()

class ChatModel(models.Model):
    '''Model for chat'''
    sender = models.ForeignKey(SenderModel, on_delete=models.CASCADE)
    receiver = models.ForeignKey(ReceiverModel, on_delete=models.CASCADE)
    text = models.TextField()
    log = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender.user.get_username()} chats {self.receiver.user.get_username()}'
    
    class Meta:
        indexes = [
            models.Index(fields=['receiver']),
            models.Index(fields=['receiver', 'is_read']),
            models.Index(fields=['sender']),
        ]
    
class ChatKeyModel(models.Model):
    '''Contains the chat key that will be used for group name on channel layer'''
    key = models.UUIDField(default=uuid4)
    usernames = models.JSONField(default=list)

    def __str__(self):
        text = 'Users: '
        for count, username in enumerate(self.usernames):
            text += username + ', '
        # Return without ', ' at last
        return text[:len(text) - 2]
    
    @classmethod
    def get_by_usernames(cls, usernames):
        chatkeys = cls.objects.all()
        usernames.sort()
        for chatkey in chatkeys:
            chatkey.usernames.sort()
            if chatkey.usernames == usernames:
                return chatkey
            