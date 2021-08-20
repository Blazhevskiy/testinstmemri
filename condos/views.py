from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .serializer import CondoSerializer
from django.db import transaction
from rest_framework.response import Response
from django.http import JsonResponse
from api.people_api.people_api import people_api

@action(
    detail=False,
    methods=['POST'],
    url_path='api/v1/import',
    url_name='import-condos',
    authentication_classes=(),
    permission_classes=(AllowAny,),
)
def import_condos(request):
    condos = people_api.run(    condo_serializer = CondoSerializer(data=condos, many=True)
    condo_serializer.is_valid(raise_exception=True)

    with transaction.atomic():
        condo = condo_serializer.save()

    return JsonResponse({'data': condos})
