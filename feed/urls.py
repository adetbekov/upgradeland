from django.conf.urls import url
import feed.views

urlpatterns = [
	url(r'^comments$', feed.views.postcomments, name="postcomments"),
	url(r'^like$', feed.views.likepost, name="likepost"),
	url(r'^create$', feed.views.createpost, name="createpost"),
	url(r'^createcomment$', feed.views.createcomment, name="createcomment"),
	url(r'^hide$', feed.views.hidepost, name="hidepost"),
	url(r'^hidecomment$', feed.views.hidecommentpost, name="hidecommentpost"),
	url(r'^(?P<page>\w+)$', feed.views.index, name="feedpage"),
    url(r'^$', feed.views.index, name="feed"),
]