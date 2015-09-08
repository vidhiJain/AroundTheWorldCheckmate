from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^register/$', views.register, name='register'),
	url(r'^check_user/$', views.check_user, name='check_user'),
	url(r'^user_status/$', views.user_status, name='user_status'),
	url(r'^exit_game/$', views.exit_game, name='exit_game'),
	url(r'^lboard/$', views.lboard, name='lboard'),
	url(r'^fly_to/$', views.fly_to, name='fly_to'),
	url(r'^submit/$', views.submit, name='submit'),
	url(r'^loc_distr/$', views.loc_distr, name='loc_distr'),
]
