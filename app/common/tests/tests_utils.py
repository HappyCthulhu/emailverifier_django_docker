from django.test import TestCase

from .. import utils


class TestFormattingPhone(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.phone1 = '9195192456'
        cls.phone2 = '79195192456'
        cls.phone3 = '+79195192456'
        cls.phone4 = '+79195192456доп764'

    def test_formatting_phone1(self):
        formatted_phone = utils.formatting_phone(phone=self.phone1)
        self.assertEqual('+7 (919) 519 24 56', formatted_phone)

    def test_formatting_phone2(self):
        formatted_phone = utils.formatting_phone(phone=self.phone2)
        self.assertEqual('+7 (919) 519 24 56', formatted_phone)

    def test_formatting_phone3(self):
        formatted_phone = utils.formatting_phone(phone=self.phone3)
        self.assertEqual('+7 (919) 519 24 56', formatted_phone)

    def test_formatting_phone4(self):
        formatted_phone = utils.formatting_phone(phone=self.phone4)
        self.assertEqual('+79195192456доп764', formatted_phone)
