from django.contrib import admin
from .models import Board

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
	model = Board
	list_display = ('title','user','content','created','visible')
	search_fields = ['title','user','content']

admin.site.register(Board, BoardAdmin)