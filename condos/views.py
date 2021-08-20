import logging

from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .serializer import (
    ModelCondoSerializer, ModelAddressSerializer, ModelEmailSerializer, ModelPhoneSerializer, ModelAmenitySerializer,
    ModelOrganizationSerializer
)
from django.db import transaction
from django.http import JsonResponse
from api.people_api.people_api import people_api


logger = logging.getLogger(__name__)


@action(
    detail=False,
    methods=['POST'],
    url_path='api/v1/import',
    url_name='import-condos',
    authentication_classes=(),
    permission_classes=(AllowAny,),
)
def import_condos(request):
    condos = people_api.run()
    for condo_data in condos:
        # try:
        with transaction.atomic():
            condo_serializer = ModelCondoSerializer(data=condo_data['condo'])
            condo_serializer.is_valid(raise_exception=True)
            condo = condo_serializer.save()

            if condo_data.get("addresses"):
                address_serializer = ModelAddressSerializer(
                    data=condo_data["addresses"], context={'condo': condo}, many=True
                )
                address_serializer.is_valid(raise_exception=True)
                address_serializer.save()

            if condo_data.get("phones"):
                phone_serializer = ModelPhoneSerializer(
                    data=condo_data["phones"], context={'condo': condo}, many=True
                )
                phone_serializer.is_valid(raise_exception=True)
                phone_serializer.save()

            if condo_data.get("emails"):
                email_serializer = ModelEmailSerializer(
                    data=condo_data["emails"], context={'condo': condo}, many=True
                )
                email_serializer.is_valid(raise_exception=True)
                email_serializer.save()

            if condo_data.get("organizations"):
                email_serializer = ModelOrganizationSerializer(
                    data=condo_data["organizations"], context={'condo': condo}, many=True
                )
                email_serializer.is_valid(raise_exception=True)
                email_serializer.save()

            if condo_data.get("amenities"):
                amenity_serializer = ModelAmenitySerializer(data=condo_data["amenities"], many=True)
                amenity_serializer.is_valid(raise_exception=True)
                amenities = amenity_serializer.save()
                condo.amenities.add(*amenities)

        # except Exception as e:
        #     logger.error(f"Something went wrong! {e}")
        #     continue

    return JsonResponse({'status': 'Import complete'})
