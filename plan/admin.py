from django.contrib import admin
from .models import MyTask, Plan

class MyTaskAdmin(admin.ModelAdmin):
	model = MyTask
	list_display = ('plan','user','title','created','first','second')
	search_fields = ['user','title']
	list_filter = ('first','second')

admin.site.register(MyTask, MyTaskAdmin)

class PlanAdmin(admin.ModelAdmin):
	model = Plan
	list_display = ('user','title','created','ended')
	search_fields = ['user','title']

admin.site.register(Plan, PlanAdmin)