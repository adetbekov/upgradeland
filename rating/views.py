from django.shortcuts import render
from .models import Rate

# Create your views here.
def index(request):
	context={
		"ratings": Rate.objects.filter(visible=True).order_by("-created")
	}
	return render(request,"rating.html",context)