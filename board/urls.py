from django.conf.urls import url
import board.views

urlpatterns = [
	url(r'^hide$', board.views.hide, name="hideboard"),
	url(r'^create$', board.views.create, name="createboard"),
    url(r'^$', board.views.index, name="board"),
]