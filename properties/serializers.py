# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Property, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = ['id', 'image']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    owner_name = serializers.SerializerMethodField()
    owner_phone = serializers.SerializerMethodField()
    governorate_name = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'property_type',
            'listing_type', 'price', 'currency', 'area',
            'bedrooms', 'bathrooms', 'governorate', 'district',
            'governorate_name', 'district_name',
            'living_rooms', 'majlis', 'kitchens',
            'images', 'owner_name', 'owner_phone'
        ]

    def get_owner_name(self, obj):
        return obj.owner.get_full_name() or obj.owner.username

    def get_owner_phone(self, obj):
        return obj.owner.profile.phone_number if hasattr(obj.owner, 'profile') else None

    def get_governorate_name(self, obj):
        return obj.governorate.name if obj.governorate else None

    def get_district_name(self, obj):
        return obj.district.name if obj.district else None
