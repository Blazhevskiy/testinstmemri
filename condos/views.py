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
    list_all_data = people_api.run()
    for condo_data in list_all_data:
        condo_data_dict = {'condo_name': condo_data[0]}
        print(condo_data_dict)
        condo_serializer = CondoSerializer(data=condo_data_dict)
        condo_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            condo = condo_serializer.save()

    return Response(data=condo)
