from django.urls import path
from .views import (
    ListUserRegistrations,
    MyObtainTokenPairView,
    RegisterView,
    PasswordResetView,
    PasswordResetConfirmView,
    UserNameValidateView,
    FollowUser,
    UserUpdateView,
    UserSearchView,
    ListAdminUsers,
    UserDetailView,
    UserOTPVerificationView,
    UserOTPSendView,
    UserProfileView,
    UserProducts,
    UserTypeView,
    UserDelete,
)


urlpatterns = [
    path("api/check-username/", UserNameValidateView.as_view(), name="check_user_name"),
    path("api/register/", RegisterView.as_view(), name="auth_register"),
    path("api/otp/send/", UserOTPSendView.as_view(), name="otp_send"),
    path("api/otp/verify/", UserOTPVerificationView.as_view(), name="otp_verification"),
    path("api/login/", MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("api/password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "api/password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("api/follow/", FollowUser.as_view(), name="password_reset_confirm"),
    path("api/user/update/", UserUpdateView.as_view(), name="user-update"),
    path("api/user/delete/", UserDelete.as_view(), name="user-delete"),
    path("api/user/search/", UserSearchView.as_view(), name="user-search"),
    path("api/user/<int:user_id>/", UserDetailView.as_view(), name="user-detail"),
    path("api/user/profile/", UserProfileView.as_view(), name="user-profile"),
    path("api/user/products/", UserProducts.as_view(), name="user-products"),
    path("api/user/type/", UserTypeView.as_view(), name="user-type"),
    ###################################### ADMIN #################################################
    path("api/admin-users/", ListAdminUsers.as_view(), name="list-admin-users"),
    path(
        "api/user-registrations/",
        ListUserRegistrations.as_view(),
        name="user-registrations",
    ),
]
