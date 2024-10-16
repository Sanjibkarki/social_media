from django.shortcuts import render
from django.views import View
from django.http import HttpResponseNotFound
from django.views.generic import ListView
from .models import PostX,Likes
from Home.models import ChatModel,SenderModel,ReceiverModel
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView,RetrieveAPIView,DestroyAPIView,RetrieveUpdateAPIView
from .serializer import Serializer,Myserializer,chatSerializer
import json
from rest_framework.response import Response

class Create(ListCreateAPIView):
    queryset = Likes.objects.all()
    serializer_class = Serializer

    def perform_create(self,serializer):
        request = self.request
        serializer.save(profile = request.user)

    def get_queryset(self,*args,**kwargs):
        qs = super().get_queryset(*args,**kwargs)
        request = self.request
        user = request.user
        if not user.is_authenticated:
            return product.objects.none()
        return qs

        
class Retrieve(RetrieveAPIView):
    queryset = PostX.objects.all()
    serializer_class = Serializer
    lookup_field = "pk"

    def get(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(self.queryset, id=pk)

        try:
            like_instance = instance.likes.get(profile = request.user)            
            serialized_data = Serializer(like_instance).data
            return Response(serialized_data)
        except Likes.DoesNotExist:
            return Response(None)
        

class Delete(DestroyAPIView):
    queryset = PostX.objects.all()
    serializer_class = Serializer
    lookup_field = "pk"

    def get(self, request, pk):
        try:
            post = self.get_object()
            like = post.likes.get(profile=request.user)
            like.delete()
            return Response({"method": "delete Item successful"})
        except PostX.DoesNotExist:
            raise HttpResponseNotFound("PostX object does not exist.")
        except Likes.DoesNotExist:
            raise HttpResponseNotFound("Like object does not exist.")
        
class Count(RetrieveAPIView):
    queryset = PostX.objects.all()
    serializer_class = Myserializer
    
    def get(self,request,pk):
        qs = super().get_queryset()
        queryset = qs.get(id=pk)
        count = queryset.likes.all().count()
        return Response({"count": count})


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
