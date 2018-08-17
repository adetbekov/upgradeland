from django.conf.urls import url
import library.views

urlpatterns = [
	# url(r'^accept/(?P<user>\w+)/$', cabinet.views.accepttask, name="accepttask"),
	# url(r'^check/(?P<user>\w+)/$', cabinet.views.checktask, name="checktask"),
	# url(r'^checks/(?P<lesson>\w+)/(?P<user>\w+)/$', cabinet.views.checklist, name="checklist"),
	# url(r'^checks/(?P<lesson_id>\w+)$', cabinet.views.checks, name="checks"),
	# url(r'^attendance/(?P<lesson>\w+)$', cabinet.views.attendance, name="attendance"),
	# url(r'^pa/(?P<lesson>\w+)$', cabinet.views.put_attendance, name="put_attendance"),
	# url(r'^caeser/$', cabinet.views.caeser, name="caeser"),
	# url(r'^hw/(?P<lesson>\w+)$', cabinet.views.hw, name="hw"),
	url(r'^(?P<shelf_id>\w+)$', library.views.shelf, name="shelf"),
    url(r'^$', library.views.index, name="library"),
]