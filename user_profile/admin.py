from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(SMSVerification)
admin.site.register(DeactivateUser)
admin.site.register(NationalIDImage)
