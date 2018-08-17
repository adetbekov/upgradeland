from django.conf.urls import url
import events.views

urlpatterns = [
    url(r'^$', events.views.index, name="events"),
]