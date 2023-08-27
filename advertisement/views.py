from django.shortcuts import render
from rest_framework import generics, status, filters
from django.http import QueryDict
from products.pagination import FilterPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Advertisement
from .serializers import AdvertisementRetriveSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.permessions import IsAdmin, IsSuperAdmin


class UserAdvertisement(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AdvertisementRetriveSerializer
    pagination_class = FilterPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['status']

    def get_queryset(self):
        queryset = Advertisement.objects.filter(customer=self.request.user)
        return queryset
    

class AdvertisementDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementRetriveSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'adv_id'


######################################################## ADMIN #############################################################


class AdvertisementAdminListAPIView(generics.ListAPIView):
    queryset = Advertisement.objects.order_by('-id')
    serializer_class = AdvertisementRetriveSerializer
    permission_classes = (IsAdmin, )
    pagination_class = FilterPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['status']