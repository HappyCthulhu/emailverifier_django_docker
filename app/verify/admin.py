import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib import admin
from django.db.models import QuerySet

from app.verify.clients import MillionVerifierClient
from app.verify.models import Verify
from config.settings.dev import EMAIL_SENDER
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

    actions = ['verify_emails']

    @admin.action(description='Проверить почты')
    def verify_emails(self, request, qs: QuerySet):
        for email in qs:
            client = MillionVerifierClient()
            code_response = client.check_email(email=email.email)
            Verify.objects.update(
                result_code=code_response
            )


@admin.register(models.Message)
class SendMessageAdmin(admin.ModelAdmin):
    model = models.Message
    list_display = (
        'message_recipient', 'message_was_sent', 'message_text',
        'modified', 'created'
    )

    actions = ['send_message']

    @admin.action(description='Отправить сообщение')
    def send_message(modeladmin, request, qs: QuerySet):
        msg = MIMEMultipart()

        for message in qs:
            msg['From'] = EMAIL_SENDER['email']
            message_recipient = message.message_recipient.email
            msg['To'] = message_recipient
            msg['Subject'] = "Subscription"

            text = message.message_text
            msg.attach(MIMEText(text, 'plain'))

            server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
            server.login(msg['From'], EMAIL_SENDER['password'])
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()

            message.message_was_sent = True
            message.save()

            print(f"Successfully sent email to: {msg['To']}")
