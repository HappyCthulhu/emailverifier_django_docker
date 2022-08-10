import re
import string
from secrets import choice

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models, DatabaseError
# Create your models here.
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel, ShortNameModel, CodeNameModel, UidModel, UidPrimaryModel, \
    StripStringFieldsModel, ExtraJsonModel, PhoneCleanFieldModel
from user.managers import UserManager


class User(UidPrimaryModel, AbstractBaseUser, PermissionsMixin, PhoneCleanFieldModel):
    """
    Модель пользователя с аутентификацией по email без имени пользователя
    """

    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone'), max_length=32, unique=True, null=True)
    name = models.CharField(_('Имя'), max_length=128, blank=True)
    short_name = models.CharField('Краткое имя', max_length=12, default='', blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('phone',)

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token_keys(self):
        tokens = self.tokens.all()
        s = ','.join(x.key for x in tokens)
        return s

    def get_initials(self):
        """
        Получение инициалов из имени
        """
        if self.name:
            return ''.join(x[0].upper() for x in re.split(r'\s+', self.name))
        return ''

    def update_short_name_from_name_as_initials(self):
        """
        Обновление коротких имен пользователей как инициалы от имени
        """
        self.short_name = self.get_initials()
        self.save()

    def clean_fields(self, exclude=None):
        """
        Установка инициалов
        """
        super().clean_fields(exclude)
        if not self.short_name and self.name:
            self.short_name = self.get_initials()

    # @property
    # def token_urls(self):
    #     tokens = self.tokens.all()
    #     s = ','.join(['https://connexio.ru' + reverse('token_auth', args=[x.key, ]) for x in tokens])
    #     return s

    def save(self, *args, **kwargs):
        self.phone = self.clean_phone(self.phone)
        super().save(*args, **kwargs)
        # Автоматическое создание токена по-умолчанию
        Token.get_or_create_token(self)


class Company(CodeNameModel, ExtraJsonModel):
    eng_code = models.CharField('Код (eng)', max_length=32, null=True, blank=True)
    inn = models.CharField('ИНН', max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Token(TimeStampedModel):
    TOKEN_39 = 39
    TOKEN_16 = 16
    TOKEN_17 = 17
    TOKEN_TMP = 1
    TOKEN_CHOICES = (
        (TOKEN_39, 'Token39'),
        (TOKEN_16, 'Token16'),
        (TOKEN_17, 'Token17'),
        (TOKEN_TMP, 'TokenTmp'),
    )
    STATUS_DRAFT = 1
    STATUS_VERIFY = 2
    STATUS_ACTIVE = 3
    STATUS_INACTIVE = 4
    STATUS_CHOICES = (
        (STATUS_DRAFT, 'черновой'),
        (STATUS_VERIFY, 'на проверке'),
        (STATUS_ACTIVE, 'активен'),
        (STATUS_INACTIVE, 'отключен'),

    )
    key = models.CharField('Токен', max_length=64)
    key_type = models.SmallIntegerField('Тип', choices=TOKEN_CHOICES, default=TOKEN_39)
    expire = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='tokens', verbose_name=_('Токены'), on_delete=models.CASCADE)
    status = models.SmallIntegerField('Статус', choices=STATUS_CHOICES, default=STATUS_DRAFT)
    verify_code = models.CharField('Код подтверждения', max_length=32, blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.get_key_type_display(), self.key.upper())

    @classmethod
    def get_user(cls, key):
        token = cls.objects.get(key=key)
        if token.expire and token.expire <= timezone.now():
            raise User.DoesNotExist()
        return token.user

    @classmethod
    def _generate_token(cls, size, alphabet):
        return ''.join(choice(alphabet) for _ in range(size))

    @classmethod
    def generate_token(cls, key_type=TOKEN_39):
        if key_type == cls.TOKEN_39:
            token = cls._generate_token(10, string.ascii_lowercase + string.digits + '_')
        elif key_type == cls.TOKEN_16:
            token = cls._generate_token(16, string.ascii_uppercase + string.ascii_lowercase + string.digits + '_')
        elif key_type == cls.TOKEN_17:
            token = cls._generate_token(17, string.ascii_uppercase + string.ascii_lowercase + string.digits + '_')
        elif key_type == cls.TOKEN_TMP:
            token = cls._generate_token(12, string.ascii_uppercase + string.ascii_lowercase + string.digits + '_')
        return token

    @classmethod
    def get_or_create_token(cls, user, key_type=TOKEN_39):
        try:
            token = Token.objects.get(user=user, key_type=key_type)
        except Token.DoesNotExist:
            token = Token(user=user, key_type=key_type)
            # if key_type == cls.TOKEN_TMP:
            #     token.expire = timezone.now() + timedelta(seconds=960)
            #     token.verify_code = cls._generate_token(4, string.digits)
            while True:
                token.key = cls.generate_token(key_type)
                try:
                    token.save()
                    break
                except DatabaseError:
                    continue
        return token

    def send_tel(self):
        if not self.user.phone:
            pass

    def send(self, to='tel'):
        if to == 'tel':
            self.send_tel()

    class Meta:
        unique_together = (
            ('key_type', 'key')
        )
