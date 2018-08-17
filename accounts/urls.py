from django.conf.urls import url
import accounts.views

urlpatterns = [
	url(r'^reanimate/(?P<user_id>\w+)/$', accounts.views.reanimate, name="reanimate"),
	url(r'^delete/(?P<user_id>\w+)/$', accounts.views.delete, name="delete"),
	url(r'^end/(?P<user_id>\w+)/$', accounts.views.endcourse, name="endcourse"),
	url(r'^profile/(?P<user_id>\w+)/$', accounts.views.profile, name="profile"),
	url(r'^activate/(?P<hash>\w+)/$', accounts.views.activate, name="activate"),
	url(r'^edituser/$', accounts.views.edituser, name="edituser"),
	url(r'^editprofile/$', accounts.views.editprofile, name="editprofile"),
	url(r'^edit/(?P<saved>\w+)/$', accounts.views.edited, name="edited"),
	url(r'^all/$', accounts.views.all, name="all"),
	url(r'^ajax/client$',accounts.views.client_ajax,name='client_ajax'),
	url(r'^edit/$', accounts.views.edit, name="edit"),
	url(r'^registration/$', accounts.views.registration, name="reg"),
    url(r'^login/$', accounts.views.login, name="login"),
    url(r'^logout/$', accounts.views.logout, name="logout"),
]