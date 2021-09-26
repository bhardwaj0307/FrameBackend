""" contains basic admin views for MultiToken """
from django.contrib import admin
from user_2FA.models import EmailOTP


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at', 'ip_address', 'user_agent')
