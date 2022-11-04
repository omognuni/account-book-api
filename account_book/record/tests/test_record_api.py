from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from book.serializers import RecordSerializer
from core.models import Record


BOOK_URL = reverse('book:book-list')

def detail_url(book_id):
    return reverse('book:book-detail', args=[book_id])

def create_record(user, **params):
    defaults = {
        'user': user,
        'amount': 10000,
        'memo': 'test memo',
    }    
    defaults.update(params)
    
    return Record.objects.create(**defaults)

def create_user(email='test@gmail.com', password='testpass'):
    return get_user_model(email=email, password=password)

class PublicAPITest(TestCase):
    '''비인증 사용자 테스트'''
    def setUp(self):
        self.client = APIClient()
        
    def test_auth_required(self):
        '''인증 요구 테스트'''
        user = create_user()
        
        res = self.client.get(BOOK_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateAPITest(TestCase):
    '''인증 사용자 테스트'''
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        
        self.client.force_authenticate(self.user)
        
    def test_create_record(self):
        pass
        
    