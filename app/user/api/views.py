from knox.views import LoginView as KnoxLoginView
from rest_framework.generics import RetrieveAPIView

from .authentication import LoginPasswordAuthentication
from .serializers import UserSerializer


class LoginView(KnoxLoginView):
    authentication_classes = [LoginPasswordAuthentication, ]


class UserView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
