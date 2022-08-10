from pathlib import Path

import pandas as pd
from django.db import models

from common.fields import UidForeignKey
from common.models import UidPrimaryModel, TimeStampedModel, NameModel
from verify.clients import MillionVerifierClient


def get_upload_path(instance, filename):
    return f'verify/{filename}'


class File(UidPrimaryModel, TimeStampedModel, NameModel):
    upload_file = models.FileField(upload_to=get_upload_path, verbose_name='Эксель таблица с email')

    def check_emails(self) -> None:
        """
        Проверить все email в таблице
        """
        df = self._get_data_frame()
        # Заменяю nan на None
        df_notnull = df.where(pd.notnull(df), None)
        for i, row in df_notnull.iterrows():
            # TODO нужно выполнять асинхронно
            client = MillionVerifierClient()
            email = row['email']
            code_response = client.check_email(email=email)
            Verify.objects.create(
                email=email,
                file=self,
                result_code=code_response
            )

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
    result_code = models.PositiveSmallIntegerField(choices=CODE_CHOICES)

    class Meta:
        verbose_name = 'Проверка email'
