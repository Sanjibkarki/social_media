from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect

class CustomRestrictAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_path = [reverse("login"),reverse("signup")]
            
        if request.user.is_authenticated:
            return self.get_response(request)
        
        if request.path not in allowed_path:
            if (request.path+"/") == reverse("signup"):
                return redirect("signup")
            else:
                return redirect("login")

                
        return self.get_response(request)
                
        
