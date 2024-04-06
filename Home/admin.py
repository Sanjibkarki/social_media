from django.contrib import admin
from Home.models import Profile
from accounts.models import User

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    fields = ["username"]
    inlines = [ProfileInline]

admin.site.register(User,UserAdmin)