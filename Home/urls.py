from django.urls import path,include
from .views import Index,Follow,Info,Followx,Add_New_Post,Message,Room
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import Login,Signup,Logout
urlpatterns = [
    path('',Index.as_view(),name="home"),
    path('follow/',Follow.as_view(),name="follow"),
    path('info/',Info.as_view(),name="info"),
    path('add_post/',Add_New_Post.as_view(),name="add_post"),
    path('messages/',Message.as_view(),name="message"),
    path('<int:user_id>/',Room.as_view(),name = "room"),
    path('login/',Login.as_view(),name="login"),
    path('signup/',Signup.as_view(),name="signup"),
    path('logout/',Logout.as_view(),name="logout"),
    path('follow/<int:id>/', Followx, name='follow_x'),
    path('api/',include("Post.urls"))
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
