from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^register/$', views.register, name='register'),
	url(r'^check_user/$', views.check_user, name='check_user'),
	url(r'^user_status/$', views.user_status, name='user_status'),
	url(r'^exit_game/$', views.exit_game, name='exit_game'),
]
