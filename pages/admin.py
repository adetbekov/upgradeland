from django.contrib import admin

# Register your models here.
from .models import Manual

class ManualAdmin(admin.ModelAdmin):
	model = Manual
	list_display = ('forwhome','question','answer')
	search_fields = ['question','answer']
	list_filter = ('forwhome',)

admin.site.register(Manual, ManualAdmin)