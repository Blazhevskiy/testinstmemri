from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Condo, Address, Amenity, Email, Phone, Organization, Group


class ModelAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

    def to_internal_value(self, data):
        data["condo"] = self.context.get("condo")
        return data


class ModelAmenitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, validators=[])

    class Meta:
        model = Amenity
        fields = "__all__"

    def create(self, validated_data):
        amenity, _ = Amenity.objects.get_or_create(**validated_data)
        return amenity


# class ModelGroupSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(required=False, validators=[])
#
#     class Meta:
#         model = Group
#         fields = "__all__"
#
#     def create(self, validated_data):
#         group, _ = Group.objects.get_or_create(**validated_data)
#         return group


class ModelEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = "__all__"

    def to_internal_value(self, data):
        data["condo"] = self.context.get("condo")
        return data


class ModelPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = "__all__"

    def to_internal_value(self, data):
        data["condo"] = self.context.get("condo")
        return data


class ModelOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"

    def validate(self, attr):
        if not any((attr.get("title"), attr.get("name"))):
            raise ValidationError("At least one field is required")
        return attr

    def to_internal_value(self, data):
        data["condo"] = self.context.get("condo")
        return data


class ModelCondoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condo
        exclude = ["amenities"]

    def create(self, validated_data):
        condo, _ = Condo.objects.get_or_create(**validated_data)
        return condo
