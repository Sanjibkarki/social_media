from django.urls import path,include
from .views import Chatseen,Index,Update
urlpatterns = [
    path('index/',Index.as_view(),name='index'),
    path('chatseen/<int:pk>/',Chatseen.as_view(),name='chatseen'),
    path('like/<int:pk>/',Update.as_view(),name='detail'),

]