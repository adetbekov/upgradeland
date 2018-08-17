from django.shortcuts import render, redirect
from .models import Manual

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return redirect("feed")
	return render(request,"index.html")

def manual(request):
	context = {}
	context["both_manuals"] = Manual.objects.filter(forwhome="B")
	if(request.user.is_staff):
		context["manuals"] = Manual.objects.filter(forwhome="S")
	else:
		context["manuals"] = Manual.objects.filter(forwhome="U")
	return render(request,'faq.html',context)