from django.contrib import admin
from Post.models import Likes,PostX
from accounts.models import User

class LikesInline(admin.StackedInline):
    model = Likes
    extra = 0

class PostAdmin(admin.ModelAdmin):
    fields = ["profile","image"]
    inlines = [LikesInline]

admin.site.register(PostX,PostAdmin)