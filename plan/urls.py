from django.conf.urls import url
import plan.views

urlpatterns = [
	url(r'^createplan/$', plan.views.createplan, name="createplan"),
	url(r'^delete/(?P<id>\w+)/$', plan.views.delete, name="deleteplan"),
	url(r'^createtask/(?P<plan_id>\w+)/$', plan.views.create, name="createtask"),
	url(r'^checksecond/(?P<user>\w+)/$', plan.views.checksecond, name="checksecondplan"),
	url(r'^checkfirst/(?P<user>\w+)/$', plan.views.checkfirst, name="checkfirst"),
	url(r'^checks/(?P<user>\w+)/$', plan.views.checklist, name="checksecond"),
	url(r'^checks$', plan.views.checks, name="planchecks"),
    url(r'^$', plan.views.index, name="plan"),
]