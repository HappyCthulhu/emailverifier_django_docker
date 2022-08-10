from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from .. import models


class MyTestCase(TestCase):
    """Базовый класс для тестов. Создаёт среду тестирования"""

    @classmethod
    def setUpTestData(cls):
        cls.admin_email = 'admin@gmail.com'
        cls.password = 'password'
        cls.admin = get_user_model().objects.create_user(email=cls.admin_email, password=cls.password, phone='12345')
        cls.admin.set_password(cls.password)

        cls.admin.is_active = True
        cls.admin.is_staff = True
        cls.admin.is_superuser = True
        cls.admin.save()


class TokenAuthTest(MyTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_url = reverse_lazy('token_auth', kwargs={'key': models.Token.objects.get(user=cls.admin).key})
