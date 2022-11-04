from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Book


def create_user(email='user@example.com', password='testpass123'):
    '''user 생성'''
    return get_user_model().objects.create_user(email, password)

class ModelTest(TestCase):
    '''모델 생성 테스트'''
    
    def test_create_user_model(self):
        '''새로운 유저 생성'''
        email = 'test@gmail.com'
        password = 'testpass'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_noramilize_email(self):
        '''이메일 소문자 변환'''
        email = 'test@GMAIL.COM'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(email.lower(), user.email)

    def test_email_validation(self):
        '''이메일 없이 가입 시 에러'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                '',
                password='testpass'
            )

    def test_create_superuser(self):
        '''superuser 생성'''
        email = 'test@gmail.com'
        password = 'testpass'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        
    def test_create_book(self):
        '''가계부 내역 생성'''
        user = create_user()
        amount = 10000
        memo = 'test memo'
        book = Book.objects.create(user=user, amount=amount, memo=memo)
        
        self.assertEqual(book.user, user)
        self.assertEqual(book.amount, amount)
        
        