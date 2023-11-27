from django.urls import path
from rest_framework.response import Response

from .views import GetTokenResetPasswordView, ResetPasswordView

urlpatterns = [
    path('get-token-reset-password', GetTokenResetPasswordView.as_view(), name='get_token_reset_password'),
    path('reset', ResetPasswordView.as_view(), name='reset_password'),
]