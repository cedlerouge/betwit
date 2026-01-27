from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import RegisterView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    # JWT token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # Registration
    path('register/', RegisterView.as_view(), name='register'),
    # Password reset
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
