from django.core.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ResetPasswordToken
from User.models import User
from .utils import sendResetPasswordEmail


class GetTokenResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        ResetPasswordToken.delete_tokens_espired()
        email = request.data.get('email')
        try:
            if not email:
                return Response({"error": "The email is required."}, status=status.HTTP_400_BAD_REQUEST)
            try:    
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'The user does not exist.'}, status=status.HTTP_401_UNAUTHORIZED)
            if user.is_active:
                if user.is_temporarily_inactive:
                        return Response({'detail': 'The user is temporarily inactive.'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    reset_password_token = ResetPasswordToken.get_or_create(user=user)
                    #sendResetPasswordEmail(reset_password_token=reset_password_token)
                    return Response({"detail": f"the token {reset_password_token.token} has been sent to {user.email}."}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'The user is not active.'}, status=status.HTTP_401_UNAUTHORIZED)  
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_401_UNAUTHORIZED)


class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        ResetPasswordToken.delete_tokens_espired()
        token = request.data.get('token')
        password = request.data.get('password')
        email = request.data.get('email')

        try:
            if not email:
                return Response({"error": "The email is required."}, status=status.HTTP_400_BAD_REQUEST)
            try:    
                user = User.objects.get(email=email)
                reset_token = ResetPasswordToken.objects.get(token=token)
            except Exception as e:
                return Response({'error': 'the user does not exist or the token was not generated with this user'}, status=status.HTTP_401_UNAUTHORIZED)
            if user.is_active:
                if user.is_temporarily_inactive:
                        return Response({'detail': 'The user is temporarily inactive.'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    if token == reset_token.token:
                        try:
                            validate_password(password)
                        except ValidationError as e:
                            errors = [str(message) for message in e.messages]
                            return Response({"detail": errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
                        user.set_password(password)
                        user.save()
                        reset_token.delete()
                        return Response({"detail": "Password has been updated."}, status=status.HTTP_200_OK)
                    else:
                        reset_token.increment_tries()
                        return Response({"detail": "The token is not valid."}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'The user is not active.'}, status=status.HTTP_401_UNAUTHORIZED)  
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_401_UNAUTHORIZED)
