from django.conf.urls import url
import pages.views

urlpatterns = [
	# url(r'^main$', pages.views.main, name="main"),
	# url(r'^follow$', pages.views.follow, name="follow"),
	url(r'^faq/$', pages.views.manual, name="faq"),
    url(r'^$', pages.views.index, name="index"),
]