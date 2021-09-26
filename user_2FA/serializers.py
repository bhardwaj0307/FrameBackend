from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

__all__ = [
    'EmailSerializer',
    'TokenSerializer',
]


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})


class TokenSerializer(serializers.Serializer):
    otp = serializers.IntegerField(label=_("Email OTP"), style={'input_type': 'text'})
