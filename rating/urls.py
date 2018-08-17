from django.conf.urls import url
import rating.views

urlpatterns = [
    url(r'^$', rating.views.index, name="rating"),
]