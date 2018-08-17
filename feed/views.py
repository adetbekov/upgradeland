from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, PostLike, PostComment
from django_ajax.decorators import ajax

# Create your views here.
@login_required
def index(request,page=1):
	context = {}
	posts = Post.objects.filter(visible=True).order_by("-id")
	paginator = Paginator(posts, 10)
	try:
		posts = paginator.page(page)
		context["page"] = page
	except PageNotAnInteger:
		posts = paginator.page(1)
		context["page"] = 1
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
		context["page"] = paginator.num_pages
	context["posts"] = posts
	context["num_pages"] = paginator.num_pages
	return render(request, "feed.html", context)


@login_required
def createpost(request):
	if request.POST:
		if "image" in request.FILES:
			image = request.FILES["image"]
		else:
			image = None
		content = request.POST["content"]
		splitcontent = ' '.join(content.split())
		if image==None and not splitcontent:
			pass
		else:
			post = Post.objects.create(user=request.user,content=content,image=image)
	return redirect("feed")
	
@login_required
def hidepost(request):
	if request.POST:
		post = Post.objects.get(id=request.POST["post"])
		if request.user == post.user or request.user.is_staff:
			post.visible = False
			post.save()
			return redirect("feed")
	return redirect("feed")

@login_required
@ajax
def likepost(request):
	liked = False
	if request.GET:
		post = Post.objects.get(id=request.GET.get("post"))
		postlike = PostLike.objects.filter(post=post,user=request.user)
		if postlike.exists():
			postlike.delete()
			liked = False
		else:
			PostLike.objects.create(post=post,user=request.user) 
			liked = True
		return {"count":PostLike.objects.filter(post=post).count(),"liked":liked}

@login_required
@ajax
def postcomments(request):
	context={}
	if request.GET:
		context["comments"]=PostComment.objects.filter(post__id=request.GET.get("post"),visible=True).order_by('-id')
		return render(request,"postcomment.html",context)

@login_required
def hidecommentpost(request):
	if request.POST:
		comment = PostComment.objects.get(id=request.POST["comment"])
		if request.user == comment.user or request.user.is_staff:
			comment.visible = False
			comment.save()
			return redirect("feed")

@login_required
@ajax
def createcomment(request):
	if request.GET:
		comment = request.GET.get("comment")
		post = Post.objects.get(id=request.GET.get("post"))
		splitcomment = ' '.join(comment.split())
		if splitcomment:
			PostComment.objects.create(user=request.user,comment=comment,post=post)
			return {"count":PostComment.objects.filter(post=post,visible=True).count()}
		else:
			return {"count":None}