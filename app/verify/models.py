from pathlib import Path

import pandas as pd
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.common.fields import UidForeignKey
from app.common.models import UidPrimaryModel, TimeStampedModel, NameModel
from app.verify.clients import MillionVerifierClient


def get_upload_path(instance, filename):
    return f'verify/{filename}'


class File(UidPrimaryModel, TimeStampedModel, NameModel):
    upload_file = models.FileField(upload_to=get_upload_path, verbose_name='Эксель таблица с email')

    def check_emails(self) -> None:
        df = self._get_data_frame()
        # Заменяю nan на None
        df_notnull = df.where(pd.notnull(df), None)
        for _, row in df_notnull.iterrows():
            email = row['email']
            code_response = client.check_email(email=email)

            email_obj = Verify.objects.create(
                email=email,
                file=self,
                result_code=code_response
            )

            if code_response == 1:
                Message.objects.create(
                    message_recipient=email_obj,
                    message_was_sent=False
                )

    FILE_STATUSES = (
        ('new', 'Новый'),
        ('processed', 'Обработан'),
        ('error', 'Ошибка'),
        ('processing', 'Добавляется в базу')
    )

    status = models.CharField(max_length=32, choices=FILE_STATUSES, default='new', blank=True)

    def _get_data_frame(self) -> pd.DataFrame:
        return pd.read_excel(Path(self.upload_file.path))

    class Meta:
        verbose_name = 'Таблицы с email'


class Verify(UidPrimaryModel, TimeStampedModel):
    CODE_OK = 1
    CODE_CATCH_ALL = 2
    CODE_UNKNOWN = 3
    CODE_ERROR = 4
    CODE_DISPOSABLE = 5
    CODE_INVALID = 6

    CODE_CHOICES = (
        (CODE_OK, 'Ok'),
        (CODE_CATCH_ALL, 'Catch All'),
        (CODE_UNKNOWN, 'Unknown'),
        (CODE_ERROR, 'Error'),
        (CODE_DISPOSABLE, 'Disposable'),
        (CODE_INVALID, 'Invalid'),
    )

    file = UidForeignKey(File, on_delete=models.CASCADE, verbose_name='Таблица с email', null=True, blank=True)
    email = models.EmailField('Проверяемый email', max_length=512)
    result_code = models.PositiveSmallIntegerField(choices=CODE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.email} - {self.result_code}'

    class Meta:
        verbose_name = 'Проверка email'


class Message(UidPrimaryModel, TimeStampedModel):
    message_text = models.TextField('Текст сообщения', max_length=4096, blank=True)
    message_was_sent = models.BooleanField(default=False, verbose_name='Сообщение отправлено')
    message_recipient = models.ForeignKey(Verify, on_delete=models.CASCADE, verbose_name='Получатель', null=True,
                                          blank=True, limit_choices_to={'result_code': Verify.CODE_OK})

    class Meta:
        verbose_name = 'Отправка message'


@receiver(post_save, sender=File)
def verify_file(sender, instance, created, **kwargs):
    if created:
        print('Some File Detected')
        try:
            if instance.status == 'new':

                instance.status = 'processing'
                instance.save()

                instance.check_emails()
                instance.status = 'processed'
                instance.save()

        except Exception as e:
            print(f'{e.__class__.__name__}: {e}')
            instance.status = 'error'
            instance.save()


client = MillionVerifierClient()