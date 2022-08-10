from django.contrib import admin

from . import models


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    # TODO добавить отображение количества связанных проверок и их кодов ответов
    model = models.File
    list_display = (
        'name',
        'upload_file',
        'modified', 'created'
    )
    ordering = ('modified',)


@admin.register(models.Verify)
class VerifyAdmin(admin.ModelAdmin):
    model = models.Verify
    list_display = (
        'file', 'email', 'result_code',
        'modified', 'created'
    )
