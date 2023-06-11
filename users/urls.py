from django.urls import path
from .views import MyObtainTokenPairView, RegisterView, UserDeleteView, UserUpdateView, SendSMS


urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='token_refresh'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='token_refresh'),
    path('send_sms/', SendSMS.as_view(), name='send_sms'),
]