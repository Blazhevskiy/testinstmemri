from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .serializer import CondoSerializer
from django.db import transaction
from rest_framework.response import Response
from api.people_api.people_api import people_api
# Create your views here.

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
    data = []
    for condo in condos:
        if "names" in condo:
            data.append({'displayName': condo['names'][0]['displayName']})
    condo_serializer = CondoSerializer(data=data, many=True)
    condo_serializer.is_valid(raise_exception=True)

    with transaction.atomic():
        condo = condo_serializer.save()

    return Response(data=condo)
