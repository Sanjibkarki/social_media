from django.contrib import admin
from Home.models import Profile,ReceiverModel,SenderModel,ChatModel,ChatKeyModel
from accounts.models import User

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    fields = ["username"]
    inlines = [ProfileInline]

admin.site.register(User,UserAdmin)
admin.site.register(ReceiverModel)
admin.site.register(SenderModel)
admin.site.register(ChatModel)
admin.site.register(ChatKeyModel)


