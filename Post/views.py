from django.shortcuts import render
from django.views import View
from django.http import HttpResponseNotFound
from django.views.generic import ListView
from .models import PostX,Likes
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView,RetrieveAPIView,DestroyAPIView
from .serializer import Serializer,Myserializer
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
    