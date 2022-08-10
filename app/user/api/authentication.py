from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from ..models import Token


class LoginPasswordAuthentication(BaseAuthentication):
    """
    HTTP Basic authentication against username/password.
    """
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        """
        """
        userid = request.data.get('username')
        password = request.data.get('password')
        return self.authenticate_credentials(userid, password, request)

    def authenticate_credentials(self, userid, password, request=None):
        """
        Authenticate the userid and password against username and password
        with optional request for context.
        """
        credentials = {
            get_user_model().USERNAME_FIELD: userid,
            'password': password
        }
        user = authenticate(request=request, **credentials)

        if user is None:
            raise AuthenticationFailed(_('Invalid username/password.'))

        if not user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

        return (user, None)


class BaseTokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Proxy-Authorization"
    HTTP header, prepended with the string "{keyword} ".  For example:

    Proxy-Authorization: Token16 em41123u54px1emm or Proxy-Authorization: Token39 v12gsdd38lm64
    """
    keyword: str = None
    model: Token = None

    def get_model(self):
        if self.model is not None:
            return self.model
        return Token

    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        auth = self.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    @staticmethod
    def get_authorization_header(request):
        """
        Return request's 'Proxy-Authorization:' header, as a bytestring.

        Hide some test client ickyness where the header can be unicode.
        """
        auth = request.META.get('HTTP_PROXY_AUTHORIZATION', b'')
        if isinstance(auth, str):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

    def authenticate_credentials(self, key):
        model = self.get_model()
        token_types = {v: k for k, v in Token.TOKEN_CHOICES}
        try:
            token = model.objects.select_related('user').get(key=key, key_type=token_types[self.keyword])
        except model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

        return token.user, token

    def authenticate_header(self, request):
        return self.keyword


class Token16Authentication(BaseTokenAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Proxy-Authorization"
    HTTP header, prepended with the string "Token16 ".  For example:

        Authorization: Token16 emm-15u54px1emm
    """

    keyword = 'Token16'


class Token39Authentication(BaseTokenAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Proxy-Authorization"
    HTTP header, prepended with the string "Token37 ".  For example:

        Authorization: Token39 emm-15u54px1
    """

    keyword = 'Token39'
