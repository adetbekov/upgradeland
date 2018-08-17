from django.shortcuts import render
import calendar
from datetime import datetime

# Create your views here.
def index(request):
	context = {}
	days = []
	a = calendar.Calendar(0)
	context["calendar"] = a.monthdayscalendar(datetime.now().year, datetime.now().month)
	return render(request,"calendar.html",context)