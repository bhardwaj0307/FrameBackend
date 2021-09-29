""" URL Configuration for core auth
"""
from django.conf.urls import url, include
from .views import *

app_name = 'Address'

urlpatterns = [
    url(r'^create_address/', create_address, name="create_address"),
    url(r'^update_address/(?P<address_id>[0-9]+)/', update_address, name="update_address"),
    url(r'^get_all_addresses/', get_all_address, name="get_all_addresses"),
    url(r'^address/(?P<address_id>[0-9]+)/', address_by_id, name="get_address"),
    url(r'^address/delete/(?P<address_id>[0-9]+)/', delete_address_by_id, name="delete_address"),
    url(r'^profile/edit/', profile_update, name="profile_update"),

]
