import random
import re
import string
import uuid

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext as _

from . import managers


class TimeStampedModel(models.Model):
    """
    Модель с датой и временем создания и изменения
    """
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('Когда создан'))
    modified = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Когда изменён'))

    class Meta:
        abstract = True


class TimestampLocalModel(models.Model):
    """
    Временная метка с локальным временем
    """
    ts = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    tz_offset = models.SmallIntegerField('Смещение временной зоны', null=True)
    ts_local = models.DateTimeField('Локальное время', null=True, blank=True)

    class Meta:
        abstract = True


class ShortNameModel(models.Model):
    """
    Объект с кратким именем

    """
    short_name = models.CharField(_('Краткое наименование'), max_length=128, blank=True)

    class Meta:
        abstract = True


class NameModel(models.Model):
    """
    Объект с именем
    """
    name = models.CharField(_('Наименование'), max_length=4096, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class CodeModel(models.Model):
    """
    Объект с кодом

    """
    code = models.CharField(_('Код'), max_length=256, blank=True)

    class Meta:
        abstract = True


class CodeNameModel(CodeModel, NameModel):
    """
    Объект с именем и кодом
    """

    def __str__(self):
        return self.name if self.code == '' else self.code

    class Meta:
        abstract = True


class UidModel(models.Model):
    """
    Объект с уникальным идентификатором
    """
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class UidPrimaryModel(models.Model):
    """
    Объект с UUID первичным ключём
    """
    uid = models.UUIDField('Уникальный идентификатор', default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        abstract = True


class IsActiveModel(models.Model):
    """
    Активность
    """
    is_active = models.BooleanField('Акстивно', default=True)

    class Meta:
        abstract = True


class NumModel(models.Model):
    """
    Целочисленное поле num, используется для сортировки
    """
    num = models.IntegerField('Число', null=True, blank=True)

    class Meta:
        abstract = True


class StripStringFieldsModel(models.Model):
    """ Strip text fields"""

    def clean(self):
        super().clean()
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name)
                if CODE(value) == 'str':
                    _value = value.strip()
                    if _value != value:
                        setattr(self, field.name, value)
                # setattr(self, field.name, None if value == '' else value)
                # if value:
                #     setattr(self, field.name, value.strip())

    class Meta:
        abstract = True


class PhoneCleanFieldModel(models.Model):

    @classmethod
    def clean_phone(cls, value):
        value = str(value).strip()
        phone = re.sub('[^0-9]', '', str(value))
        if len(phone) == 0:
            return ''
        if phone[0] == '8':
            phone = '7' + phone[1:]
        elif value[0] in ('+', '7',):
            pass
        else:
            phone = '7' + phone
        return phone

    class Meta:
        abstract = True


class ExtraJsonModel(models.Model):
    extra_json = models.JSONField('Extra JSON', default=dict, blank=True)

    class Meta:
        abstract = True


class ExtraTxtModel(models.Model):
    extra_txt = models.TextField('Расширенный текст', blank=True)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    class Meta:
        abstract = True


class SidModel(models.Model):
    sid = models.CharField('SID', max_length=5, null=True, blank=True, unique=True, editable=False)
    sid_prefix = 'u'
    sid_alphabet = string.ascii_lowercase + '123456789'

    def get_sid_prefix(self):
        return self.sid_prefix

    def get_sid_alphabet(self):
        return self.sid_alphabet

    def _generate_sid(self):
        prefix = self.get_sid_prefix()
        abc = self.get_sid_alphabet()
        for x in range(1000):
            sid = prefix + str(now().year)[-1] + ''.join(random.choice(abc) for i in range(3))
            if not self._meta.managers[0].filter(sid=sid).exists():
                return sid
        raise Exception('Ошибка! Не могу сгенерировать уникальный код SID')

    class Meta:
        abstract = True


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = managers.SoftDeletionManager()
    all_objects = managers.SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        self.save()

    def hard_delete(self):
        super().delete()


try:
    from ordered_model.models import OrderedModelBase


    class OrderedModel(OrderedModelBase):
        """
        An abstract model that allows objects to be ordered relative to each other.
        Provides an ``order`` field.
        """

        num = models.PositiveIntegerField('№ п/п', editable=False, db_index=True)
        order_field_name = "num"

        class Meta:
            abstract = True
            ordering = ("num",)
except ImportError as e:
    pass
