from django.urls import path

# from knox import views as knox_views
from .views import UserView

urlpatterns = [
    path('user', UserView.as_view(), name='user_info'),
]
