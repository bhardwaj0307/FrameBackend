from django.conf.urls import url

from user_custom.api import views

app_name = "users_api"
urlpatterns = [
    url(r'^user/$', views.UsersApiCreateRead.as_view({"get": "get_all_user"}), name='get_user'),
    url(r'^create_user/$', views.UsersApiCreateRead.as_view({"post": "create_user"}), name='create_user'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UsersApiCreateRead.as_view({"get": "specific_user"}), name='specific_user'),
    url(r'^user/delete/(?P<pk>[0-9]+)/$', views.UsersApiCreateRead.as_view({"delete": "delete_user"}),
        name='delete_user'),
    url(r'^user/edit/$', views.UsersApiCreateRead.as_view({"put": "edit_user"}), name='edit_user'),
    url(r'^log_in/$', views.UsersApiCreateRead.as_view({"get": "get_current_user"}), name='get_current_user'),
    url(r'^users_details/$', views.UsersApiCreateRead.as_view({"get": "get_users_exclude_logged_user"}),
        name='get_users_exclude_logged_user'),
    url(r'^(?P<user_id>[0-9]+)/(?P<user_status>[0-9]+)/$',
        views.UsersApiCreateRead.as_view({"post": "change_status_of_user"}), name='change_status_of_user'),
    url(r'^registered_emails/$', views.UsersApiCreateRead.as_view({"get": "check_email_admin"}),
        name='get_registered_email'),

]
