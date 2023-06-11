from django.shortcuts import render
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import RegisterSerializer, UserUpdateSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .permessions import IsAdmin
from django.contrib.auth.hashers import check_password


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
    

from .services import send_sms    
class SendSMS(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        send_sms('+919633854889', 'OTP: 667892')
        return Response({'sucess':'message sucess'})