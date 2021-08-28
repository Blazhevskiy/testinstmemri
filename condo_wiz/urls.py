"""condo_wiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from authorization.views import CustomerViewSet
from condos import views

from django.urls import path, include
from django.conf import settings
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import routers
from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.views import ManagementViewSet



schema_view = get_schema_view(
   openapi.Info(
      title="Condo_wiz",
      default_version='v1',
      description="Test entire scope of APIs",
   ),
   public=True,
   permission_classes=(AllowAny, ),
   generator_class=OpenAPISchemaGenerator
)

router = routers.SimpleRouter()
router.trailing_slash = '/?'
router.register(r'', ManagementViewSet, basename='management')
router.register(r'', CustomerViewSet, basename='customer')

urlpatterns = [
    path('api/v1/', include((router.urls, 'v1'), namespace='v1')),
]

if settings.DEBUG:
    urlpatterns += [
        # Docs for APIs
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('admin/', admin.site.urls),
        path('api/v1/import', views.import_condos),
   ]
