from rest_framework import serializers
from .models import Advertisement


class AdvertisementRetriveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = '__all_'