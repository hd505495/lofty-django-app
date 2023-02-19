# from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import KeyValue


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

class KeyValueList(generics.ListAPIView):
    model = KeyValue
    queryset = KeyValue.objects.all()

class KeyValueCreate(APIView):
    # def __init__(self, request, key):
    #     self.request = request
    #     self.key = key

    def post(self, request):
        key = request.key
        id = KeyValue.objects.create(key=key)

        return Response(id, status.HTTP_201_CREATED);

class KeyValueIncrement(APIView):
    def __init__(self, request, key):
        self.request = request
        self.key = key

    def get_object(self):
        return get_object_or_404(KeyValue, key=self.key)

    def post(self, request):
        obj = self.get_object()
        obj.value += 1
        obj.save()

        return Response('', status.HTTP_200_OK)