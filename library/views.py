from django.shortcuts import render
from .models import Shelf, Book
# Create your views here.
def index(request):
	context = {
		"shelves" : Shelf.objects.filter(hidden=False).order_by("-created")
	}
	return render(request, "library.html", context)

def shelf(request,shelf_id):
	context = {
		"shelf" : Shelf.objects.get(id=shelf_id)
	}
	return render(request, "shelf.html", context)