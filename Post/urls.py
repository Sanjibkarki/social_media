from django.urls import path,include
from .views import Create,Retrieve,Delete,Count
urlpatterns = [
    path('create/', Create.as_view(), name='create'),
    path('retrieve/<int:pk>/',Retrieve.as_view(),name='retrieve'),
    path('delete/<int:pk>/',Delete.as_view(),name='delete'),
    path('count_likes/<int:pk>/',Count.as_view(),name='count')
]