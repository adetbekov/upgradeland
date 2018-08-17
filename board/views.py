from django.shortcuts import render, redirect
from .models import Board
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
	context={
		"boards" : Board.objects.filter(visible=True).order_by("-id")
	}
	return render(request,'board.html',context)

@login_required
def hide(request):
	if request.POST:
		board = Board.objects.get(id=request.POST["b"])
		if request.user == board.user or request.user.is_staff:
			board.visible = False
			board.save()
			return redirect("board")
	return redirect("board")

@login_required
def create(request):
	if request.POST:
		if request.POST["title"]:
			splitcontent = ' '.join(request.POST["content"].split())
			if not splitcontent:
				pass
			else:
				Board.objects.create(title=request.POST["title"],content=request.POST["content"],user=request.user)
	return redirect("board")