from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django_ajax.decorators import ajax
from .models import MyTask, Plan
from cabinet.models import Stream
from datetime import datetime, timedelta

@login_required
def index(request):
	if not Plan.objects.filter(user=request.user).exists():
		context={
			"new" : True,
			"students" : Stream.objects.filter().order_by("-created")[0].students.all().filter(profile__ended__isnull=True).exclude(profile__user=request.user)
		}	
	elif Plan.objects.filter(user=request.user).order_by("-created")[0].ended != None:
		context={
			"students" : Stream.objects.filter().order_by("-created")[0].students.all().filter(profile__ended__isnull=True).exclude(profile__user=request.user),
			"finishedplan" : Plan.objects.filter(user=request.user).order_by("-created")[0],
			"tasks": MyTask.objects.filter(plan=Plan.objects.filter(user=request.user).order_by("-created")[0],user=request.user),
			"date":datetime.today()-datetime(year=Plan.objects.filter(user=request.user).order_by("-created")[0].created.year,month=Plan.objects.filter(user=request.user).order_by("-created")[0].created.month,day=Plan.objects.filter(user=request.user).order_by("-created")[0].created.day),
		}
	elif datetime(year=Plan.objects.filter(user=request.user).order_by("-created")[0].created.year,month=Plan.objects.filter(user=request.user).order_by("-created")[0].created.month,day=Plan.objects.filter(user=request.user).order_by("-created")[0].created.day) + timedelta(days=14) < datetime.now():
		context={
			"students" : Stream.objects.filter().order_by("-created")[0].students.all().filter(profile__ended__isnull=True).exclude(profile__user=request.user),
			"date":datetime(year=Plan.objects.filter(user=request.user).order_by("-created")[0].created.year,month=Plan.objects.filter(user=request.user).order_by("-created")[0].created.month,day=Plan.objects.filter(user=request.user).order_by("-created")[0].created.day) + timedelta(days=14),
			"failedplan" : Plan.objects.filter(user=request.user).order_by("-created")[0],
			"tasks": MyTask.objects.filter(plan=Plan.objects.filter(user=request.user).order_by("-created")[0],user=request.user),
		}
	else:
		plan = Plan.objects.filter(user=request.user).order_by("-created")[0]
		if MyTask.objects.filter(plan=plan).exists():
			if MyTask.objects.filter(plan=plan,second=False).count() == 0:
				plan.ended = datetime.now()
				plan.save()
				return redirect("plan")
		context={
			"date":datetime(year=Plan.objects.filter(user=request.user).order_by("-created")[0].created.year,month=Plan.objects.filter(user=request.user).order_by("-created")[0].created.month,day=Plan.objects.filter(user=request.user).order_by("-created")[0].created.day) + timedelta(days=14),
			"plan" : plan,
			"tasks": MyTask.objects.filter(plan=plan,user=request.user)
		}
	return render(request,"plan.html",context)

@login_required
def create(request,plan_id):
	plan = Plan.objects.get(id=plan_id)
	if request.POST:
		if request.POST["title"]:
			splitcontent = ' '.join(request.POST["title"].split())
			if not splitcontent:
				pass
			else:
				MyTask.objects.create(plan=plan,title=request.POST["title"],user=request.user)
	return redirect("plan")

@login_required
def createplan(request):
	if request.POST:
		if request.POST["title"]:
			splitcontent = ' '.join(request.POST["title"].split())
			if not splitcontent:
				pass
			else:
				if request.POST["viewers"]:
					viewers = request.POST["viewers"].split(",")
					plan = Plan.objects.create(title=request.POST["title"],user=request.user)
					for viewer in viewers:
						plan.viewer.add(User.objects.get(username=viewer))
	return redirect("plan")


@login_required
def delete(request,id):
	task = MyTask.objects.get(id=id)
	if task.user == request.user:
		task.delete()
	return redirect("plan")

@login_required
@ajax
def checkfirst(request,user):
	checked = False
	u=User.objects.get(id=user)
	if request.GET:
		task = MyTask.objects.get(id=request.GET.get("task"))
		if task.first:
			task.first=False
			task.second=False
			checked = False
		else:
			task.second=False
			task.first=True
			checked = True
		task.save()
		return {"checked":checked}

@login_required
def checks(request):
	unchecked_users = []
	checked_users = []
	context = {}
	if Plan.objects.filter(viewer=request.user,ended__isnull=True).exists():
		plan = Plan.objects.filter(viewer=request.user,ended__isnull=True).order_by("-created")[0]
		checked = MyTask.objects.filter(plan=plan,second=True,first=True).order_by("-created")
		unchecked = MyTask.objects.filter(plan=plan,second=False,first=True).order_by("-created")

		for item in unchecked:
			unchecked_users.append(item.user)
		unchecked_users_set=set(unchecked_users).union(unchecked_users)
		for item in unchecked_users_set:
			item.count=unchecked.filter(user=item.id,first=True, second=False).count()

		for item in checked:
			checked_users.append(item.user)
		checked_users_set=set(checked_users).union(checked_users)
		for item in checked_users_set:
			item.count=checked.filter(user=item.id,first=True, second=True).count()
		context={
			'checked': checked_users_set,
			'unchecked': unchecked_users_set,
		}
	return render(request,"viewer.html",context)

@login_required
def checklist(request,user):
	context = {}
	if Plan.objects.filter(viewer=request.user,user__id=user).exists():
		if Plan.objects.filter(viewer=request.user,user__id=user).order_by("-created")[0].ended == None:
			plan = Plan.objects.filter(viewer=request.user,user__id=user).order_by("-created")[0]
			context={
				"plan": plan,
				"user": User.objects.get(id=user),
				"tasks": MyTask.objects.filter(plan=plan),
				"date": datetime(year=plan.created.year,month=plan.created.month,day=plan.created.day) + timedelta(days=14),
			}
	return render(request,"checklistplan.html",context)


@login_required
@ajax
def checksecond(request,user):
	checked = False
	u=User.objects.get(id=user)
	if request.GET:
		task = MyTask.objects.get(id=request.GET.get("task"))
		print(task)
		if task.first:
			if task.second:
				task.second=False
				checked = False
			else:
				task.second=True
				checked = True
		else:
			if task.second:
				task.second=False
				task.first=False
				checked = False
			else:
				task.second=True
				task.first=True
				checked = True
		task.save()
		return {"checked":checked}