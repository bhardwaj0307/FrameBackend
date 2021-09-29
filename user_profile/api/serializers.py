from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from rest_framework import serializers, exceptions
from phonenumber_field.serializerfields import PhoneNumberField
from drf_extra_fields.fields import Base64ImageField
from user_profile.models import Profile, Address, SMSVerification, DeactivateUser, NationalIDImage

UserModel = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CreateAddressSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        if "phone_number" in data:
            if data["phone_number"] == "":
                data["phone_number"] = None
        return super(CreateAddressSerializer, self).to_internal_value(data)

    class Meta:
        model = Address
        exclude = ["user", "country"]


class UpdateAddressSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        if "phone_number" in data:
            if data["phone_number"] == "":
                data["phone_number"] = None
        return super(UpdateAddressSerializer, self).to_internal_value(data)

    class Meta:
        model = Address
        exclude = ["user", "country"]
