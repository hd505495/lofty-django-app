import json, os
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.files.temp import NamedTemporaryFile
from django.test import TestCase
from rest_framework.test import APIRequestFactory
import PIL.Image
from unittest.mock import patch

from .models import DogImage, KeyValue
from .views import keyvalue_create, keyvalue_increment, keyvalue_list, dogs_generate, dog_get


class KeyValueAPITestCase(TestCase):

    async def test_keyvalue_create(self):
        view = keyvalue_create
        factory = APIRequestFactory()
        request = factory.post('/api/keys/', {'key': 'blue'}, format='json')
        response = await view(request)

        data = json.loads(response.content) if response.content else None
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertEqual(data['key'], 'blue')
        self.assertEqual(await KeyValue.objects.acount(), 1)
        kv = await KeyValue.objects.afirst()
        self.assertEqual(kv.key, 'blue')
        self.assertEqual(kv.value, 0)

    async def test_keyvalue_create_no_key(self):
        view = keyvalue_create
        factory = APIRequestFactory()
        request = factory.post('/api/keys/')
        response = await view(request)

        data = json.loads(response.content) if response.content else None
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(data)
        self.assertEqual(await KeyValue.objects.acount(), 0)

    async def test_keyvalue_increment(self):
        view = keyvalue_increment
        factory = APIRequestFactory()
        key = 'green'
        await KeyValue.objects.acreate(key=key)
        request = factory.post(f"/api/keys/{key}/increment/")
        response = await view(request, key)

        data = json.loads(response.content) if response.content else None
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)

        self.assertEqual(data, {key: 1})
        self.assertEqual(await KeyValue.objects.acount(), 1)
        kv = await KeyValue.objects.afirst()
        self.assertEqual(kv.key, key)
        self.assertEqual(kv.value, 1)

    async def test_keyvalue_increment_bad_key(self):
        view = keyvalue_increment
        factory = APIRequestFactory()
        key = 'brown'
        request = factory.post(f"/api/keys/{key}/increment")
        response = await view(request, key)

        data = json.loads(response.content) if response.content else None
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(data)
        self.assertEqual(await KeyValue.objects.acount(), 0)

    async def test_keyvalue_list(self):
        view = keyvalue_list
        factory = APIRequestFactory()
        await KeyValue.objects.acreate(key='circle')
        await KeyValue.objects.acreate(key='square')
        await KeyValue.objects.acreate(key='triangle')
        request = factory.get(f"/api/keys/list/")
        response = await view(request)

        data = json.loads(response.content) if response.content else None
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 3)
        self.assertIn({'key': 'circle', 'value': 0}, data)
        self.assertIn({'key': 'square', 'value': 0}, data)
        self.assertIn({'key': 'triangle', 'value': 0}, data)

class DogImageAPITestCase(TestCase):

    def test_dogs_generate(self):
        view = dogs_generate
        factory = APIRequestFactory()
        request = factory.post('/api/dogs/generate/')
        self.assertEqual(DogImage.objects.count(), 0)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(DogImage.objects.count(), 24)

        dog_images = DogImage.objects.all()
        for image_obj in dog_images:
            self.assertIsNotNone(type(image_obj.image))
            self.assertIsNotNone(type(image_obj.filename))
            self.assertIsNotNone(type(image_obj.height))
            self.assertIsNotNone(type(image_obj.width))
            self.assertIsNotNone(type(image_obj.format))
            self.assertIsNotNone(type(image_obj.mode))
            self.assertIsNotNone(type(image_obj.bits))
            self.assertIsNotNone(type(image_obj.layers))


    def test_dog_get(self):
        factory = APIRequestFactory()
        dogs_generate(factory.post('/api/dogs/generate/'))

        with patch.object(PIL.Image.Image, 'transpose') as mock_transpose:

            view = dog_get
            request = factory.get('/api/dog/')

            response = view(request)
            self.assertEqual(response.status_code, 200)

            mock_transpose.assert_called_once()

            data = json.loads(response.content) if response.content else None
            self.assertEqual(len(data), 3)

            modified_image_url = data.get('modified', '')
            original_image_url = data.get('original', '')
            original_metadata = data.get('metadata', {})

            self.assertIn('/flipped/', modified_image_url)
            self.assertNotEqual(modified_image_url, original_image_url)
            self.assertNotEqual(len(original_metadata), 0)
