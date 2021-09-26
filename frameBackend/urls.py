"""enterprise_pro URL Configuration

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
import time
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.conf.urls import include, url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase


# from oklance_auth.utils.email_verification import email_verification_request_token


def time_function():
    return int(time.time())


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         # Add custom claims
#         timestamp = time_function()
#         user_email_status = user.is_email_verified
#         if user_email_status:
#             user_plus_timestamp = str(user.roles) + str(timestamp) + str(1)
#         else:
#             user_plus_timestamp = str(user.roles) + str(timestamp) + str(0)
#         token['state'] = user_plus_timestamp
#         # ...
#
#         return token


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


# class CustomSerializer(TokenObtainPairSerializer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields[self.username_field] = serializers.EmailField()
#         self.fields['password'].required = False
#
#     def validate(self, attrs):
#         attrs.update({'password': ''})
#         return super(CustomSerializer, self).validate(attrs)
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         # Add custom claims
#         timestamp = time_function()
#         user_email_status = user.is_email_verified
#         if user_email_status:
#             user_plus_timestamp = str(user.roles) + str(timestamp) + str(1)
#         else:
#             user_plus_timestamp = str(user.roles) + str(timestamp) + str(0)
#         token['state'] = user_plus_timestamp
#         # ...
#
#         return token
#
#
#
#
# class EmailOnlyToken(TokenObtainPairView):
#     serializer_class = CustomSerializer


schema_view = get_schema_view(
    openapi.Info(
        title="Education Market Place API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

third_party_urls = [
                       url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                           name='schema-json'),
                       url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                       url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                       path('admin/', admin.site.urls),
                       path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                       path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                       path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
                       url(r'^api/password_reset/',
                           include('django_rest_passwordreset.urls', namespace='password_reset')),
                       # path('api/email_verification/',
                       #      email_verification_request_token, name='email_verification'),

                   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

installed_apps_urls = [
                          url(r'^api/v1/users/', include('user_custom.api.urls', namespace='users_api')),
                          # url(r'^api/v1/users_data/', include('user_profile.urls', namespace='users_api')),
                          url(r'^api/password_change/',
                              include("user_custom.api.forget_password_urls", namespace='api')),
                          # url(r'^api/email_verify/',
                          #     include("user_custom.api.email_verification_urls", namespace='email_api')),
                      ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = third_party_urls + installed_apps_urls

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
