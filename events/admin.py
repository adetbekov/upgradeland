from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
	model = Event
	list_display = ('title','description','date','visible')
	search_fields = ['title','description']
	list_filter = ('visible',)

admin.site.register(Event, EventAdmin)