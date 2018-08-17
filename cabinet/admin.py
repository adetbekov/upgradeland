from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from redactor.widgets import RedactorEditor
from .models import Stream, Lesson, Attendance, HomeTask, CheckedTask
  
class StreamAdmin(admin.ModelAdmin):
	model = Stream
	list_display = ('name','description','created')
	search_fields = ['name','students','description']
	filter_horizontal = ('students',)

admin.site.register(Stream, StreamAdmin)

class LessonForm(forms.ModelForm):
	class Meta:
		model = Lesson
		fields = '__all__'
		widgets = {
		   'content': RedactorEditor(),
		   'hw': RedactorEditor(),
		}

class HomeTaskInline(admin.TabularInline):
    model = HomeTask
    extra = 0

class LessonAdmin(admin.ModelAdmin):
	form = LessonForm
	list_display = ('name','stream','day','description','created','visible')
	search_fields = ['name','content','content','hw','description','stream']
	list_filter = ('stream','visible',)
	inlines = [HomeTaskInline]

admin.site.register(Lesson, LessonAdmin)

class AttendanceAdmin(admin.ModelAdmin):
	model = Attendance
	list_display = ('lesson','user','created','attended')
	search_fields = ['lesson','user__username','user__first_name','user__last_name','user__email']
	list_filter = ('attended',)

admin.site.register(Attendance, AttendanceAdmin)

class HomeTaskAdmin(admin.ModelAdmin):
	model = HomeTask
	list_display = ('lesson','name','created','visible',)

admin.site.register(HomeTask,HomeTaskAdmin)

class CheckedTaskAdmin(admin.ModelAdmin):
	model = CheckedTask
	list_display = ('task','user','created','second')

admin.site.register(CheckedTask,CheckedTaskAdmin)