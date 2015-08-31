from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^register/$', views.register, name='register'),
	url(r'^check_user/$', views.check_user, name='check_user'),
	url(r'^send_init_data/$', views.send_init_data, name='send_init_data'),
	url(r'^exit_game/$', views.exit_game, name='exit_game'),
]
