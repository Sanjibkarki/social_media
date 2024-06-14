from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm,SignUpForm
from django.contrib.auth import authenticate,logout,login
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from accounts.models import User
from django.contrib.auth.views import PasswordResetConfirmView 

@method_decorator(cache_control(no_store = True,no_cache=True), name='dispatch')

class Login(View):
    def get(self,request):
        return render(request,"authentication/login.html")
    
    def post(self,request,*args, **kwargs):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user  = authenticate(request,email=email,password = password)
            if user is not None:
                login(request,user)
                return redirect("home")
            else:
                return redirect("login")
        return render(request, "authentication/login.html", {"errors": form.errors})
@method_decorator(cache_control(no_store = True,no_cache=True), name='dispatch')
class Signup(View):
    def get(self,request):
        return render(request,"authentication/signup.html")
    
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = User(
                email=form.cleaned_data.get("email"),
                username=form.cleaned_data.get("username"),
            )
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            auth_user = authenticate(request,username = form.cleaned_data.get("email"),password = form.cleaned_data.get("password"))
            login(request, user)
            return redirect("/")
            
        else:
         
            if 'email' in form.errors:
                return render(request, "authentication/signup.html", {"errors1": form.errors['email']})
            elif 'username' in form.errors:
                return render(request, "authentication/signup.html", {"errors2": form.errors['username']})
            elif 'password' in form.errors:
                return render(request, "authentication/signup.html",{"errors3": form.errors['password']})
            elif 'confirm_password' in form.errors:
                return render(request, "authentication/signup.html",{"errors4": form.errors['confirm_password']})
                
                

@method_decorator(cache_control(no_store = True,no_cache=True), name='dispatch')

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect("login")
