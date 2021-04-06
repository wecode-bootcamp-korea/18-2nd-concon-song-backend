from django.urls import path
from .views      import SocialAccountView

urlpatterns = [
    path('/social-login',SocialAccountView.as_view()),
]