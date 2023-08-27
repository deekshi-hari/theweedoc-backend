from django.urls import path
from .views import *

urlpatterns = [
    path('api/advs/list/', UserAdvertisement.as_view(), name='advs-list'),
    path('api/advs//<int:adv_id>/', AdvertisementDetailView.as_view(), name='advs-detail'),

]