from django.shortcuts import render
from django.views import View
from django.http import HttpResponseNotFound
from django.views.generic import ListView
from .models import PostX
from rest_framework import status
from accounts.models import User
from Home.models import ChatModel,SenderModel,ReceiverModel
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView,RetrieveAPIView,DestroyAPIView,RetrieveUpdateAPIView,ListAPIView
from .serializer import Myserializer,chatSerializer
import json
from rest_framework.response import Response
from django.core.paginator import Paginator

class Index(ListAPIView):
    serializer_class = Myserializer

    def get(self, request, *args, **kwargs):
        try:
            following_post = request.user.profile.follows.all().values_list('user', flat=True)
            queryset = PostX.objects.filter(profile__in=following_post).order_by('-date_of_post')
            paginator = Paginator(queryset, 3) 
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            serializer = Myserializer(page_obj.object_list, many=True, context={'request': request}).data
            return Response({
            'posts': serializer,
            'has_next': page_obj.has_next(),
        })
        except PostX.DoesNotExist:
            serializer = {}
            return Response({
            'posts': serializer,
            'has_next': False,
        })

class Chatseen(RetrieveUpdateAPIView):
    queryset = ChatModel.objects.all()
    serializer_class = chatSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.is_read = True
            instance.save()
        
        serializer = self.get_serializer(instance)  
        return Response(serializer.data)

class Update(RetrieveUpdateAPIView):
    queryset = PostX.objects.all()
    serializer_class = Myserializer
    lookup_field = 'pk'
    
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field)
        try:
            
            post = self.get_object() 
            if request.user in post.liked_by.all():
                post.liked_by.remove(request.user)
                post.save()
                
            else:
                post.liked_by.add(request.user)
                post.save()  
                
            totalLikes = post.liked_by.all().count()
            return Response({"likes": totalLikes}, status=status.HTTP_200_OK)

        except PostX.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
