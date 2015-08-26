from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^register/$', views.register, name='register'),
	url(r'^check_user/$', views.check_user, name='check_user')
]
