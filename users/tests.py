from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Type, Permission
from users.serializers import TypeSerializer

class TypeTestCase(APITestCase):
    def setUp(self):
        # Create permissions
        self.permission_read = Permission.objects.create(name='Read', identifier='R')
        self.permission_write = Permission.objects.create(name='Write', identifier='W')

        # Create a type
        self.type = Type.objects.create(name='Admin')
        self.type.permissions.add(self.permission_read, self.permission_write)

    def test_create_type(self):
        url = reverse('type-list')
        data = {'name': 'Editor', 'permissions': [self.permission_read.pk, self.permission_write.pk]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Type.objects.count(), 2)
        self.assertEqual(Type.objects.get(name='Editor').permissions.count(), 2)

    def test_read_type(self):
        url = reverse('type-detail', kwargs={'pk': self.type.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TypeSerializer(self.type).data)

    def test_update_type(self):
        url = reverse('type-detail', kwargs={'pk': self.type.pk})
        data = {'name': 'SuperAdmin'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.type.refresh_from_db()
        self.assertEqual(self.type.name, 'SuperAdmin')

    def test_delete_type(self):
        url = reverse('type-detail', kwargs={'pk': self.type.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Type.objects.count(), 0)
