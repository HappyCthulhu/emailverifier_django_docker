import re
import string

from django.contrib.auth.backends import ModelBackend

from user.models import Token, User


class UrlTokenBackend(ModelBackend):
    def authenticate(self, request, key=None):
        try:
            if key:
                alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '_'
                key = key.strip()
                key = re.sub('[^' + alphabet + ']', '', key)
            user = Token.get_user(key=key)
        except (User.DoesNotExist, Token.DoesNotExist):
            return None

        if not user.is_active:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
