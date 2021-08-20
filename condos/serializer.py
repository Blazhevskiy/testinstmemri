from django.conf import settings
from rest_framework import serializers
from .models import Condos, Location
BATCH_SIZE = 500


class CondoSerializer(serializers.Serializer):
    displayName = serializers.CharField(source='condo_name', max_length=64, required=True)
    picture = serializers.CharField(max_length=500, default=None)
    location = serializers.IntegerField(required=False)
    street_name = serializers.CharField(max_length=64, required=True)
    street_address = serializers.CharField(max_length=64, required=True)
    district = serializers.CharField(max_length=64, default=None)
    province = serializers.CharField(max_length=64, required=True)
    zip_code = serializers.CharField(max_length=64)
    note = serializers.CharField(max_length=2000, default=None)
    description = serializers.CharField(max_length=2000, required=True)
    amenities = serializers.CharField(max_length=500, default=None)
    building_type = serializers.IntegerField(default=None)
    condo_type = serializers.IntegerField(required=False)
    condo_corp = serializers.CharField(max_length=64, required=True)
    floors = serializers.IntegerField()
    units = serializers.IntegerField()
    builder = serializers.IntegerField(default=None)
    architect = serializers.IntegerField(default=None)
    interior_designer = serializers.IntegerField(default=None)
    date_completed = serializers.DateTimeField(required=False)
    pm = serializers.IntegerField(default=None)
    developer = serializers.CharField(max_length=64, default=None)
    send_email = serializers.CharField(max_length=64, default=None)
    view_floor_plans = serializers.CharField(max_length=64, required=True)
    created_date = serializers.DateTimeField(default=None)
    modified_date = serializers.DateTimeField(default=None)
    created_by = serializers.IntegerField(default=None)
    modified_by = serializers.IntegerField(default=None)
    e_status = serializers.CharField(max_length=10, default='Active')

    def validate_condo(self, value):
        if Condos.objects.filter(condo_name=value).exists():
            return None
        else:
            return value

    def create(self, validated_data):
#        condos_to_create = [Condos(**validated_data) for condo in validated_data]
#        Condos.objects.bulk_create(Condos(**validated_data), batch_size=BATCH_SIZE)
        for key, value in validated_data.items():
            if key == 'location':
                validated_data[key] = Location(value)
        condo = Condos(**validated_data)
        condo.save()
        return condo
