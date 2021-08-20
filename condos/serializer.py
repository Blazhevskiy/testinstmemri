from django.conf import settings
from rest_framework import serializers
from .models import Condos

BATCH_SIZE = 500


class CondoSerializer(serializers.Serializer):
    displayName = serializers.CharField(source='condos_name', max_length=64, required=True)
    picture = serializers.CharField(max_length=500, default=None)
    location_id = serializers.IntegerField()
    street_name = serializers.CharField(max_length=64, required=True)
    street_address = serializers.CharField(max_length=64, required=True)
    district = serializers.CharField(max_length=64, default=None)
    province = serializers.CharField(max_length=64, required=True)
    zip_code = serializers.CharField(max_length=64)
    note = serializers.CharField(max_length=2000, default=None)
    description = serializers.CharField(max_length=2000, required=True)
    amenities = serializers.CharField(max_length=500, default=None)
    building_type_id = serializers.IntegerField(default=None)
    condo_type_id = serializers.IntegerField()
    condo_corp = serializers.CharField(max_length=64, required=True)
    floors = serializers.IntegerField()
    units = serializers.IntegerField()
    builder_id = serializers.IntegerField(default=None)
    architect_id = serializers.IntegerField(default=None)
    interior_designer_id = serializers.IntegerField(default=None)
    date_completed = serializers.DateTimeField(default=None)
    pm_id = serializers.IntegerField(default=None)
    developer = serializers.CharField(max_length=64, default=None)
    send_email = serializers.CharField(max_length=64, default=None)
    view_floor_plans = serializers.CharField(max_length=64, required=True)
    created_date = serializers.DateTimeField(default=None)
    modified_date = serializers.DateTimeField(default=None)
    created_by_id = serializers.IntegerField(default=None)
    modified_by_id = serializers.IntegerField(default=None)
    e_status = serializers.CharField(max_length=10, default='Active')

    def validate_condo(self, value):
        if Condos.objects.filter(condo_name=value).exists():
            return None
        else:
            return value

    def create(self, validated_data):
        condos_to_create = [Condos(**condo) for condo in validated_data]
        Condos.objects.bulk_create(condos_to_create, batch_size=BATCH_SIZE)
        return True
