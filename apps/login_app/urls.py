from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.registration),
    url(r'^authenticate$', views.auth_user),
    url(r'^success$', views.user_logged),
    url(r'^clear_session$', views.clear_session)
]