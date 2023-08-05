from django.urls import path
from .views import MyObtainTokenPairView, RegisterView, PasswordResetView, PasswordResetConfirmView, UserNameValidateView, \
                    FollowUser, UserUpdateView, UserSearchView, ListAdminUsers, UserDetailView


urlpatterns = [
    path('api/check-username/', UserNameValidateView.as_view(), name='check_user_name'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('api/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('api/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/follow/', FollowUser.as_view(), name='password_reset_confirm'),
    path('api/user/update/', UserUpdateView.as_view(), name='user-update'),
    path('api/user/search/', UserSearchView.as_view(), name='user-search'),
    path('api/user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),

    ###################################### ADMIN #################################################

    path('api/admin-users/', ListAdminUsers.as_view(), name='list-admin-users'),
]