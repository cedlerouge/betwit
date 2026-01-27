from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings

from .serializers import (
    UserRegistrationSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"

            send_mail(
                'Password Reset Request',
                f'Click the following link to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except User.DoesNotExist:
            pass

        return Response(
            {"message": "If an account exists with this email, a password reset link has been sent."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data={**request.data, 'token': token})
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"error": "Invalid reset link."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"error": "Invalid or expired reset link."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(
            {"message": "Password has been reset successfully."},
            status=status.HTTP_200_OK
        )
