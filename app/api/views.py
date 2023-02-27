# from django.shortcuts import render
import json, logging, sys

import requests, urllib

from asgiref.sync import sync_to_async
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponse, JsonResponse

from PIL import Image

from .models import KeyValue, DogImage
# from .serializers import KeyValueSerializer


def index(request):
    return HttpResponse("Welcome to lofty django app")

async def keyvalue_list(request):
    if request.method != 'GET':
        return HttpResponse(status=405)
    queryset = await sync_to_async(list)(KeyValue.objects.values())
    return JsonResponse(queryset, safe=False)

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

def dogs_generate(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    logging.basicConfig(filename='logs/error.log', encoding='utf-8', level=logging.DEBUG)

    try:
        res = requests.get('https://dog.ceo/api/breeds/image/random/24')
        res.raise_for_status()
        data = res.json()
    except requests.exceptions.HTTPError as e:
        print(e, file=sys.stderr)
        return HttpResponse(status=500)

    dogs = data['message']

    if len(dogs) == 0:
        return HttpResponse(status=500)

    for dog_img_url in dogs:
        filename = dog_img_url.split('/')[-1]

        img_temp = NamedTemporaryFile(delete=True)
        with urllib.request.urlopen(dog_img_url) as uo:
            img_temp.write(uo.read())
            img_temp.flush()
        image_file = File(img_temp)
        
        image = Image.open(image_file)

        if not image:
            logging.info('failure')
            continue

        dog_image = DogImage()
        dog_image.filename = filename
        dog_image.height = getattr(image, 'height', image.size[1])
        dog_image.width = getattr(image, 'width', image.size[0])
        dog_image.format = getattr(image, 'format', None)
        dog_image.mode = getattr(image, 'mode', None)
        dog_image.frames = getattr(image, 'frames', None)
        dog_image.bits = getattr(image, 'bits', None)
        dog_image.layers = getattr(image, 'layers', None)
        dog_image.image.save(filename, image_file)
        dog_image.image_url = dog_img_url
        dog_image.save()

    return HttpResponse(status=200)

async def dog_get(request):
    pass

def dog_get(request):
    if request.method != 'GET':
        return HttpResponse(status=405)
    


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