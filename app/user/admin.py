from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Token


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Define admin model for custom User model with no email field.
    """

    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password',)}),
        (_('Personal info'), {'fields': ('name', 'short_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2'),
        }),
    )
    list_display = (
        'email', 'phone', 'short_name', 'name', 'is_staff', 'is_superuser', 'token_keys', 'date_joined')
    search_fields = ('email', 'phone', 'short_name', 'name',)
    ordering = ('date_joined',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(pk=request.user.pk)


@admin.register(Token)
class CacheAdmin(admin.ModelAdmin):
    model = Token
