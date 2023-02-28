import json, logging, sys

import requests, urllib

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from PIL import Image

from .models import DogImage, KeyValue


async def keyvalue_list(request):
    if request.method != 'GET':
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    queryset = await sync_to_async(list)(KeyValue.objects.values())
    return JsonResponse(queryset, safe=False)


async def keyvalue_create(request):
    if request.method != 'POST':
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    key = json.loads(request.body).get('key', '') if request.body else None
    if (key):
        obj = await KeyValue.objects.acreate(key=key)
        return JsonResponse({'key': obj.key})

    return HttpResponse({}, status=status.HTTP_400_BAD_REQUEST)


async def keyvalue_increment(request, key):
    if request.method != 'POST':
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
        obj = await KeyValue.objects.aget(pk=key)
    except KeyValue.DoesNotExist:
        return HttpResponse({}, status=status.HTTP_400_BAD_REQUEST)

    obj.value += 1
    await sync_to_async(obj.save)()
    return JsonResponse({obj.key: obj.value})


def dogs_generate(request):
    if request.method != 'POST':
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        res = requests.get('https://dog.ceo/api/breeds/image/random/24')
        res.raise_for_status()
        data = res.json()
    except requests.exceptions.HTTPError as e:
        print(e, file=sys.stderr)
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    dogs = data['message']

    if len(dogs) == 0:
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        dog_image.save()

        image.close()

    return HttpResponse(status=status.HTTP_200_OK)


def dog_get(request):
    if request.method != 'GET':
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    original_obj = DogImage.objects.order_by('?').first()
    original = Image.open(original_obj.image)
    flipped = original.transpose(method=Image.FLIP_TOP_BOTTOM)
    filename = f"{settings.MEDIA_DIR}/dogs/flipped/{original_obj.filename}"
    flipped.save(filename)

    modified_uri = request.build_absolute_uri(f"/media/dogs/flipped/{original_obj.filename}")
    original_uri = request.build_absolute_uri(original_obj.image.url)

    metadata = {
        'filename': original_obj.filename,
        'height': original_obj.height,
        'width': original_obj.width,
        'format': original_obj.format,
        'mode': original_obj.mode,
        'frames': original_obj.frames,
        'bits': original_obj.bits,
        'layers': original_obj.layers
    }

    return JsonResponse({
        'modified': modified_uri,
        'original': original_uri,
        'metadata': metadata
    })
