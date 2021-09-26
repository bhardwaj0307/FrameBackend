""" URL Configuration for core auth
"""
from django.conf.urls import url, include
from .views import reset_password_request_token, reset_password_confirm, reset_password_validate_token

app_name = 'email_otp'

urlpatterns = [
    url(r'^validate/', reset_password_validate_token, name="email_otp-validate"),
    url(r'^confirm_otp/', reset_password_confirm, name="email_otp-confirm"),
    url(r'^send_otp', reset_password_request_token, name="email_otp_request"),
]
