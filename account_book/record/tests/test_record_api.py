from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from record.serializers import RecordSerializer, RecordDetailSerializer
from core.models import Record


RECORD_URL = reverse('record:record-list')

def detail_url(record_id):
    return reverse('record:record-detail', args=[record_id])\

def delete_url(record_id):
    return reverse('record:record-delete', args=[record_id])

def restore_url():
    return reverse('record:record-restore')

def create_record(user, **params):
    defaults = {
        'user': user,
        'category': 'cash',
        'amount': 10000,
        'memo': 'test memo',
    }    
    defaults.update(params)
    
    return Record.objects.create(**defaults)

def create_user(email='test@gmail.com', password='testpass'):
    return get_user_model().objects.create_user(email=email, password=password)

class PublicAPITest(TestCase):
    '''비인증 사용자 테스트'''
    def setUp(self):
        self.client = APIClient()
        
    def test_auth_required(self):
        '''인증 요구 테스트'''
        user = create_user()
        
        res = self.client.get(RECORD_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateAPITest(TestCase):
    '''인증 사용자 테스트'''
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        
        self.client.force_authenticate(self.user)
        
    def test_retrieve_record(self):
        '''가계부 내역 가져오기'''
        create_record(user=self.user)
        create_record(user=self.user)
        create_record(user=self.user)
        
        res = self.client.get(RECORD_URL)
        
        records = Record.objects.all()
        serializer = RecordSerializer(records, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_record_list_limited_to_user(self):
        '''유저가 작성한 가계부 내역만 가져오기'''
        other_user = create_user(email='test2@gmail.com', password='testpass')
        create_record(user=other_user)
        create_record(user=self.user)

        res = self.client.get(RECORD_URL)

        records = Record.objects.filter(user=self.user)
        serializer = RecordSerializer(records, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_record(self):
        '''가계부 내역 생성'''
        payload = {
            'amount': 10000,
            'category': 'cash',
            'memo': 'test memo',
        }
        
        res = self.client.post(RECORD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        record = Record.objects.get(id=res.data['id'])        
        
        for k, v in payload.items():
            self.assertEqual(getattr(record, k), v)
            
    def test_view_record_detail(self):
        """가계부 상세 내역"""
        record = create_record(user=self.user)

        url = detail_url(record.id)
        res = self.client.get(url)

        serializer = RecordDetailSerializer(record)
        self.assertEqual(res.data, serializer.data)

            
    def test_partial_update(self):
        '''가계부 내역 부분 업데이트'''
        original_memo = 'test memo'
        record = create_record(
            user=self.user,
            amount=1000,
            memo=original_memo
        )

        payload = {
            'amount': 100000
        }

        url = detail_url(record.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertEqual(record.amount, payload['amount'])
        self.assertEqual(record.memo, original_memo)
        self.assertEqual(record.user, self.user)

    def test_full_update(self):
        '''가계부 내역 전체 업데이트'''
        record = create_record(
            user=self.user,
            amount=10000,
            memo='test memo'
        )

        payload = {
            'category': 'card',
            'amount': 1000,
            'memo': 'test2 memo'
        }
        url = detail_url(record.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(record, k), v)
        self.assertEqual(record.user, self.user)
        
    def test_temp_delete_record(self):
        '''가계부 임시 삭제 테스트'''
        record = create_record(user=self.user)
        
        url = delete_url(record.id)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertTrue(record.is_deleted)

    def test_retrieve_without_deleted_record(self):
        '''삭제한 내역 가져오지 않기'''
        record = create_record(user=self.user, memo='Deleted', is_deleted=True)
        create_record(user=self.user)
        
        res = self.client.get(RECORD_URL)
        serializer = RecordSerializer(record)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer.data, res.data)
        

    def test_retrieve_deleted_records(self):
        '''복구를 위한 삭제된 내역만 가져오기'''
        create_record(user=self.user)
        create_record(user=self.user)
        
        create_record(user=self.user, is_deleted=True)
        create_record(user=self.user, is_deleted=True)
        
        url = restore_url()
        res = self.client.get(url)
        
        records = Record.objects.filter(is_deleted=True)
        serializer = RecordDetailSerializer(records, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        
    def test_restore_record(self):
        '''임시 삭제 내역 복구 테스트'''
        record = create_record(user=self.user)
        record.is_deleted = True
        record.save()
                
        url = delete_url(record.id)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertFalse(record.is_deleted)
        

        
