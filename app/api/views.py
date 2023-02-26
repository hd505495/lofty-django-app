# from django.shortcuts import render
import json, logging, sys

import requests

from asgiref.sync import sync_to_async
from django.http import HttpResponse, JsonResponse
# from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
from PIL import Image
from PIL.ExifTags import TAGS

from .models import KeyValue
# from .serializers import KeyValueSerializer


def index(request):
    return HttpResponse("Welcome to lofty django app")

# @require_GET()
async def keyvalue_list(request):
    if request.method != 'GET':
        return HttpResponse(status=405)
    queryset = await sync_to_async(list)(KeyValue.objects.values())
    return JsonResponse(queryset, safe=False)

# @require_POST()
async def keyvalue_create(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    key = json.loads(request.body).get('key', '')
    if (key):
        obj = await KeyValue.objects.acreate(key=key)
        # return Response(id, status.HTTP_201_CREATED);
        return JsonResponse({'key': obj.key})

    # return Response('', status.HTTP_400_BAD_REQUEST);
    return JsonResponse({})

# @require_POST()
async def keyvalue_increment(request, key):
    if request.method != 'POST':
        return HttpResponse(status=405)
    try:
        obj = await KeyValue.objects.aget(pk=key)
    except KeyValue.DoesNotExist:
        # return Response(status.HTTP_404_NOT_FOUND)
        return JsonResponse({})
    obj.value += 1
    await sync_to_async(obj.save)()
    return JsonResponse({obj.key: obj.value})


# async def dogs_generate(request):
#     # requests.get()
#     async with aiohttp.ClientSession() as session:
#         async with session.get() as res:
#             data = await res.json()
#             print(data)

# class KeyValueList(generics.ListAPIView):
#     model = KeyValue
#     # queryset = KeyValue.objects.all()
#     serializer_class = KeyValueSerializer

#     async def get_queryset(self):
#         return await KeyValue.objects.aall()

#     async def get(self, request):
#         queryset = await self.get_queryset()
#         return queryset
#         # return await sync_to_async(super().get_queryset)()

# class KeyValueCreate(APIView):
#     # def __init__(self, request, key):
#     #     self.request = request
#     #     self.key = key

#     # def post(self, request):
#     #     print('processing post request')
#     #     key = json.loads(request.body).get('key', '')
#     #     if (key):
#     #         obj = KeyValue.objects.create(key=key)
#     #         # print(f"{obj.key}: {obj.value}")
#     #         # return JsonResponse({obj.key: obj.value});
#     #         return JsonResponse({'key': obj.key});

#     #     return JsonResponse({});

#     async def post(self, request):
#         key = json.loads(request.body).get('key', '')
#         if (key):
#             obj = await KeyValue.objects.acreate(key=key)
#             # return Response(id, status.HTTP_201_CREATED);
#             return JsonResponse({'key': obj.key})

#         # return Response('', status.HTTP_400_BAD_REQUEST);
#         return JsonResponse({})

# class KeyValueIncrement(APIView):
#     # def __init__(self, request, key):
#     #     self.request = request
#     #     self.key = key

#     # def get_object(self, key):
#     #     return get_object_or_404(KeyValue, key=key)

#     async def get_object_async(self, key):
#         try:
#             obj = await KeyValue.objects.aget(pk=key)
#             return obj
#         except KeyValue.DoesNotExist:
#             # return Response(status.HTTP_404_NOT_FOUND)
#             return JsonResponse({})

#     # def post(self, request, key):
#     #     obj = self.get_object(key)
#     #     obj.value += 1
#     #     obj.save()

#     #     return JsonResponse({obj.key: obj.value});

#     async def post(self, request, key):
#         obj = await self.get_object_async(key)
#         obj.value += 1
#         await sync_to_async(obj.save)()

#         return JsonResponse({obj.key: obj.value});
#         # return Response('', status.HTTP_200_OK)