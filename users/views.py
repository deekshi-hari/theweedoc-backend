from django.shortcuts import render
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, UserOTP
from products.models import Product
from .serializers import (
    RegisterSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    UserSerializer,
    UserSearchSerializer,
    UserUpdateSerializer,
    UsernameValidateSerializer,
    AdminUserListSerializer,
    UserDetailSerializer,
    UserTypeSerializer,
)
from products.serializers import ProductRetriveSerializer
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .permessions import IsSuperAdmin, IsAdmin
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import QueryDict
from .cloudinary_utils import upload_files
from products.pagination import FilterPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.db import models
import random


class MyObtainTokenPairView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        if "." in request.data["username"]:
            try:
                user = User.objects.get(email=request.data["username"])
            except User.DoesNotExist:
                return Response(
                    {"error": "username is invalid"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            try:
                user = User.objects.get(username=request.data["username"])
            except User.DoesNotExist:
                return Response(
                    {"error": "username is invalid"}, status=status.HTTP_404_NOT_FOUND
                )
        if check_password(request.data["password"], user.password):
            token, created = Token.objects.get_or_create(user=user)
            if user.is_active == False:
                user.is_active = True
                user.save()
            return Response({"token": token.key})
        else:
            return Response(
                {"error": "password is invalid"}, status=status.HTTP_401_UNAUTHORIZED
            )


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = []
    serializer_class = RegisterSerializer


class UserOTPSendView(APIView):

    def generate_otp(self, email):
        otp = random.randint(100000, 999999)
        if UserOTP.objects.filter(otp=otp).exists():
            return self.generate_otp(email)
        return otp

    def post(self, request, *args, **kwargs):
        email = request.data["email"]
        otp = self.generate_otp(email)
        otp_obj = UserOTP.objects.create(email=email, otp=otp)
        mail_subject = "Weedoc OTP Verification"
        message = render_to_string("otp_verification_email.html", {"otp": otp})
        email = EmailMessage(mail_subject, message, to=[request.data["email"]])
        email.content_subtype = "html"
        email.send()
        return Response({"sucess": "OTP send sucessfully"})


class UserOTPVerificationView(APIView):

    def get(self, request, *args, **kwars):
        otp = int(request.GET.get("otp"))
        user_otp_obj = UserOTP.objects.filter(otp=otp).order_by("-id")
        if user_otp_obj.count() > 0:
            if user_otp_obj[0].otp == otp:
                return Response({"sucess": "email verified"})
            else:
                return Response({"error": "wrong otp"})
        return Response({"error": "otp did not generated"})


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = get_object_or_404(User, email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        current_site = get_current_site(request)
        mail_subject = "Password Reset"
        message = render_to_string(
            "password_reset_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": str(uid),
                "token": token,
            },
        )
        email = EmailMessage(mail_subject, message, to=[email])
        email.content_subtype = "html"
        email.send()
        return Response(
            {"detail": "Password reset email has been sent"}, status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]
        uid = force_str(urlsafe_base64_decode(request.data["uid"]))
        user = get_object_or_404(User, pk=uid)

        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response(
                {"detail": "Password has been reset successfully"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "Invalid reset token"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserNameValidateView(generics.GenericAPIView):
    serializer_class = UsernameValidateSerializer

    def post(self, request, *args, **kwargs):
        user_name = request.data["username"]
        if User.objects.filter(username=user_name).exists():
            return Response({"data": "username exist"})
        return Response({"data": "valid username"})


class FollowUser(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **Kwargs):
        user = User.objects.get(id=request.user.id)
        user_to_folow = User.objects.get(username=request.data["username"])
        if user.is_following(user_to_folow):
            user.unfollow(user_to_folow)
            return Response({"sucess": "unfollowed"})
        user.follow(user_to_folow)
        return Response({"sucess": "followed"})


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        data = QueryDict("", mutable=True)
        data.update(request.data)
        if "profile_pic" in request.data.keys():
            data["profile_pic"] = ""
        if "designation" in request.data.keys():
            data["designation"] = request.data["designation"]
        if "first_name" in request.data.keys():
            data["first_name"] = request.data["first_name"]
        if "last_name" in request.data.keys():
            data["last_name"] = request.data["last_name"]
        if "dob" in request.data.keys():
            data["dob"] = request.data["dob"]
        if "gender" in request.data.keys():
            data["gender"] = request.data["gender"]
        if "location" in request.data.keys():
            data["location"] = request.data["location"]
        if "postal_code" in request.data.keys():
            data["postal_code"] = request.data["postal_code"]
        if "weblink" in request.data.keys():
            data["weblink"] = request.data["weblink"]
        serializer = self.serializer_class(data=data, partial=True)
        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            if "profile_pic" in request.data.keys():
                profile_pic = request.FILES["profile_pic"]
                if "first_name" in request.data.keys():
                    image_url = (
                        f'weedoc/profilepic/{data["first_name"]+str(request.user.id)}/'
                    )
                else:
                    image_url = (
                        f"weedoc/profilepic/{user.first_name+str(request.user.id)}/"
                    )
                resulted_image_url = upload_files(profile_pic, image_url, "image")
                data["profile_pic"] = resulted_image_url

            serializer = self.serializer_class(user, partial=True, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
            user.delete()
            return Response({"sucess": "user has been deleted"})
        except:
            return Response({"error": "user not found"})


class UserSearchView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSearchSerializer
    queryset = User.objects.exclude(email="")
    pagination_class = FilterPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "first_name", "last_name"]

    def get_serializer_context(self):
        # Get the default context data by calling the parent's method
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            followers_subquery = self.request.user.followers.all().values_list(
                "id", flat=True
            )
            followers_subquery_list = list(followers_subquery)
            context["followers_subquery_list"] = followers_subquery_list
        context["request"] = self.request
        return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # If the user is authenticated, add the 'is_following' field to the queryset
    #     if self.request.user.is_authenticated:
    #         queryset = queryset.annotate(is_following=self.request.user.following.filter(pk=models.OuterRef('pk')).exists())
    #         print(queryset)
    #     return queryset


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "id"
    lookup_url_kwarg = "user_id"

    def get_serializer_context(self):
        # Get the default context data by calling the parent's method
        context = super().get_serializer_context()
        context["request"] = self.request
        if self.request.user.is_authenticated:
            followers_subquery = self.request.user.followers.all().values_list(
                "id", flat=True
            )
            followers_subquery_list = list(followers_subquery)
            context["followers_subquery_list"] = followers_subquery_list
        return context


class UserProfileView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset

    def get_serializer_context(self):
        # Get the default context data by calling the parent's method
        context = super().get_serializer_context()
        context["request"] = self.request
        if self.request.user.is_authenticated:
            followers_subquery = self.request.user.followers.all().values_list(
                "id", flat=True
            )
            followers_subquery_list = list(followers_subquery)
            context["followers_subquery_list"] = followers_subquery_list
        return context


class UserProducts(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductRetriveSerializer
    pagination_class = FilterPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["status"]

    def get_queryset(self):
        queryset = Product.objects.filter(customer=self.request.user)
        return queryset


class UserTypeView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserTypeSerializer

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset


#################################################### ADMIN ####################################################################


class ListAdminUsers(generics.ListAPIView):
    queryset = User.objects.filter(
        Q(user_type="admin") | Q(user_type="superadmin")
    ).order_by("-id")
    permission_classes = (IsAdmin,)
    serializer_class = AdminUserListSerializer
    pagination_class = FilterPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["designation"]
    search_fields = ["phone_number", "email", "username"]


from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models.functions import TruncMonth, TruncDay, TruncHour


class ListUserRegistrations(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_trunc_and_delta(self, filter):
        filter = filter.lower()
        if filter == "yearly":
            return TruncMonth, relativedelta(years=1), "%Y-%m"
        elif filter == "monthly":
            return TruncDay, relativedelta(months=1), "%Y-%m-%d"
        elif filter == "daily":
            return TruncHour, relativedelta(days=1), " %H:%M"
        else:
            raise ValueError(
                "Invalid filter value. Use 'yearly', 'monthly', or 'daily'."
            )

    def get(self, request, *args, **kwargs):
        filter = request.GET.get("filter", "yearly")
        try:
            trunc_func, delta, date_format = self.get_trunc_and_delta(filter)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        start_date = datetime.now() - delta
        end_date = datetime.now()

        users = (
            User.objects.filter(created_at__gte=start_date, created_at__lte=end_date)
            .annotate(period=trunc_func("created_at"))
            .values("period")
            .annotate(count=Count("id"))
            .order_by("period")
        )

        data = {user["period"].strftime(date_format): user["count"] for user in users}
        return Response(data)
