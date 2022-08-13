from django.contrib import admin
from django.db.models import QuerySet

from app.verify.clients import MillionVerifierClient
from . import models


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):

    model = models.File
    list_display = (
        'name',
        'status',
        'upload_file',
        'modified',
        'created'
    )
    ordering = ('modified',)
    actions = ['add_emails_to_db', 'check_emails']

    @admin.action(description='Проверить почты')
    def check_emails(self, request, qs: QuerySet):

        for file in qs:
            # check status of file
            if file.status == 'processed':
                for email in file.verify_set.all():
                    # check email
                    client = MillionVerifierClient()
                    result = client.check_email(email.email)
                    email.result_code = result
                    email.save()


@admin.register(models.Verify)
class VerifyAdmin(admin.ModelAdmin):
    model = models.Verify

    list_display = (
        'file', 'email', 'result_code',
        'modified', 'created'
    )
