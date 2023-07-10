from django.urls import path
from .views import MyObtainTokenPairView, RegisterView, PasswordResetView, PasswordResetConfirmView, UserNameValidateView, \
                    FollowUser


urlpatterns = [
    path('api/check-username/', UserNameValidateView.as_view(), name='check_user_name'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('api/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('api/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/follow/', FollowUser.as_view(), name='password_reset_confirm'),
    # path('user/update/<int:pk>/', UserUpdateView.as_view(), name='token_refresh'),
    # path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='token_refresh'),
    # path('send_sms/', SendSMS.as_view(), name='send_sms'),
]