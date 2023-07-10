from django.shortcuts import render
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import RegisterSerializer, UserUpdateSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer, \
                            UserSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .permessions import IsAdmin
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


class MyObtainTokenPairView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response({'error': 'username is invalid'}, status=status.HTTP_404_NOT_FOUND)
        if check_password(request.data['password'], user.password):
            token, created = Token.objects.get_or_create(user=user)
            if user.is_active == False:
                user.is_active = True
                user.save()
            return Response({'token': token.key})
        else:
            return Response({'error': 'password is invalid'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = []
    serializer_class = RegisterSerializer


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAdmin,) #custom permession class
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        if 'username' in request.data:
            return Response({'error': 'username cannot be updated'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = self.get_object()
            serializer = UserUpdateSerializer(user, partial=True, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=self.kwargs['pk'])
        except User.DoesNotExist:
            return Response({'error': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return self.destroy(request, *args, **kwargs)
    

# from .services import send_sms    
# class GenerateOTP(APIView):
    
#     def post(self, request, *args, **kwargs):
#         return Response({'sucess':'message sucess'})

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        current_site = get_current_site(request)
        mail_subject = 'Password Reset'
        message = render_to_string(
            'password_reset_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': str(uid),
                'token': token,
            }
        )
        email = EmailMessage(mail_subject, message, to=[email])
        email.send()
        return Response(
            {'detail': 'Password reset email has been sent'},
            status=status.HTTP_200_OK
        )
    

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']
        uid = force_str(urlsafe_base64_decode(request.data['uid']))
        user = get_object_or_404(User, pk=uid)

        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response(
                {'detail': 'Password has been reset successfully'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'detail': 'Invalid reset token'},
            status=status.HTTP_400_BAD_REQUEST
        )
    

class UserNameValidateView(generics.GenericAPIView):
    serializer_class = UserUpdateSerializer

    def post(self, request, *args, **kwargs):
        user_name = request.data['username']
        if User.objects.filter(username=user_name).exists():
            return Response({'data': 'username exist'})
        return Response({'data': 'valid username'})


class FollowUser(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **Kwargs):
        user = User.objects.get(id=request.user.id)
        user_to_folow = User.objects.get(username=request.data['username'])
        if user.is_following(user_to_folow):
            user.unfollow(user_to_folow)
            return Response({'sucess': 'unfollowed'})
        user.follow(user_to_folow)
        return Response({'sucess': 'followed'})

