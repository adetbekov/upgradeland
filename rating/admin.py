from django.contrib import admin
from .models import Rate,Top

# Register your models here.
class TopInline(admin.TabularInline):
    model = Top
    extra = 0
    filter_horizontal = ('student',)

class TopAdmin(admin.ModelAdmin):
	model = Top
	list_display = ('ratelist','comment','place','visible')
	search_fields = ['student','ratelist','comment']
	list_filter = ('ratelist','visible','place')
	
admin.site.register(Top, TopAdmin)

class RateAdmin(admin.ModelAdmin):
	model = Rate
	list_display = ('title','created','visible')
	list_filter = ('visible',)
	search_fields = ['title',] 
	inlines = [TopInline]

admin.site.register(Rate, RateAdmin)
