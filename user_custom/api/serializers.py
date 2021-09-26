from rest_framework import serializers
from user_custom.models import User
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Enter password',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}


class PasswordTokenSerializer(serializers.Serializer):
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})
    password2 = serializers.CharField(label=_("Confirm password"), style={'input_type': 'password'})


# class ChangePasswordSerializer(serializers.Serializer):
#     model = User
#
#     old_password = serializers.CharField(
#         write_only=True,
#         required=True,
#         help_text='Enter password',
#         style={'input_type': 'password', 'placeholder': 'Password'}
#     )
#
#     new_password = serializers.CharField(
#         write_only=True,
#         required=True,
#         help_text='Enter password',
#         style={'input_type': 'password', 'placeholder': 'Password'}
#     )
#
#     confirm_password = serializers.CharField(
#         write_only=True,
#         required=True,
#         help_text='Enter password',
#         style={'input_type': 'password', 'placeholder': 'Password'}
#     )
#     email = serializers.EmailField(unique=True, null=True, error_messages={
#         'unique': _("A user with that email already exists."),
#     }, )
#
#     name = serializers.CharField(_('Full name'), max_length=150, blank=False)


# class VerifyOTPSerializer(serializers.ModelSerializer):
#     otp = serializers.IntegerField
