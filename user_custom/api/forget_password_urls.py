from django.conf.urls import url

from user_custom.api import views
app_name = "api"

urlpatterns = [
    url(r'^(?P<token_auth>[A-Za-z0-9@#$%^&+=]+)$', views.ResetPasswordConfirm.as_view({"post": "forget_password"}),
        name='forget_password'),

]
