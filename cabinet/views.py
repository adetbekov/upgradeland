from django.contrib.admin.views.decorators import staff_member_required
from .models import Stream, Lesson, Attendance, HomeTask, CheckedTask
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django_ajax.decorators import ajax
from collections import Counter
from itertools import chain

@login_required
def index(request):
	context={
		"streams": Stream.objects.filter(finished__isnull=True).order_by("-name")
	}
	return render(request,"cabinet.html",context)

@login_required
def content(request,lesson):
	context={
		"lesson": Lesson.objects.get(id=lesson)
	}
	return render(request,"content.html",context)

@login_required
def hw(request,lesson):
	context={
		"lesson": Lesson.objects.get(id=lesson),
		"tasks": HomeTask.objects.filter(lesson=lesson,visible=True)
	}
	return render(request,"hw.html",context)

@login_required
@ajax
def checktask(request,user):
	checked = False
	u=User.objects.get(id=user)
	if request.GET:
		task = HomeTask.objects.get(id=request.GET.get("task"))
		checkedtask = CheckedTask.objects.filter(task=task,user=u)
		if checkedtask.exists():
			checkedtask.delete()
			checked = False
		else:
			CheckedTask.objects.create(task=task,user=u) 
			checked = True
		return {"checked":checked}
		
@login_required
def attendance(request,lesson):
	context={
		"lesson": Lesson.objects.get(id=lesson),
		'attended': Attendance.objects.filter(lesson=lesson,attended=False),
		'absent': Attendance.objects.filter(lesson=lesson,attended=True)
	}
	return render(request,"attendance.html",context)

@login_required
@staff_member_required
def checks(request,lesson_id):
	unchecked_users = []
	checked_users = []
	lesson = Lesson.objects.get(id=lesson_id)
	checked = CheckedTask.objects.filter(task__lesson=lesson,second=True).order_by("-created")
	unchecked = CheckedTask.objects.filter(task__lesson=lesson,second=False).order_by("-created")

	for item in unchecked:
		unchecked_users.append(item.user)
	unchecked_users_set=set(unchecked_users).union(unchecked_users)
	for item in unchecked_users_set:
		item.count=unchecked.filter(user=item.id).count()

	for item in checked:
		checked_users.append(item.user)
	checked_users_set=set(checked_users).union(checked_users)
	for item in checked_users_set:
		item.count=checked.filter(user=item.id).count()
	context={
		'lesson': lesson,
		'checked': checked_users_set,
		'unchecked': unchecked_users_set,
	}
	return render(request,"checks.html",context)

@login_required
@staff_member_required
def checklist(request,lesson,user):
	context={
		"lesson": Lesson.objects.get(id=lesson),
		"user": User.objects.get(id=user),
		"tasks": HomeTask.objects.filter(lesson=lesson,visible=True)
	}
	return render(request,"checklist.html",context)

@login_required
@ajax
@staff_member_required
def accepttask(request,user):
	checked = False
	u=User.objects.get(id=user)
	if request.GET:
		task = HomeTask.objects.get(id=request.GET.get("task"))
		checkedtask = CheckedTask.objects.filter(task=task,user=u)
		if checkedtask.exists():
			check=CheckedTask.objects.get(task=task,user=u)
			if checkedtask.last().second:
				check.second=False
				checked = False
			else:
				check.second=True
				checked = True
			check.save()
		else:
			CheckedTask.objects.create(task=task,user=u,second=True) 
			checked = True
		return {"checked":checked}


############################################################

from itertools import chain
from collections import Counter

@login_required
def caeser(request):
	context={}
	alpha = 'abcdefghijklmnopqrstuvwxyz'
	often = 'etaoins'
	res = ''
	result = []
	results = []
	if request.GET:
		text = request.GET.get("text")
		texted = text.lower()
		textspaceless = ""
		for c in texted:
			textspaceless += "" if (c not in alpha) else c 
		if textspaceless!="":
			counter = Counter(chain(textspaceless))
			ordered = sorted(
			    set(textspaceless), key=lambda k: counter[k], reverse=True
			)
			context["ordered"] = ordered
			for item in ordered[:5]:
				for char in often:
					if char != item:
						k=alpha.index(item)- alpha.index(char)
						for c in text:
							try:
								res += c if c not in alpha else alpha[(alpha.index(c) - k) % len(alpha)]
							except:
								pass
						results.append({"letter": str(item + " как " + char),"text":res,"k":k})
						result.append(res)
						res = ''
			for item in ordered[:5]:
				for char in often:
					if char != item:
						k=alpha.index(char)- alpha.index(item)
						for c in text:
							try:
								res += c if c not in alpha else alpha[(alpha.index(c) - k) % len(alpha)]
							except:
								pass
						results.append({"letter": str(item + " как " + char),"text":res,"k":k})
						res = ''
			counter2 = Counter(chain(result))
			ordered2 = sorted(
			    set(result), key=lambda k: counter2[k], reverse=True
			)
			context["result"] = ordered2[0]
			context["encripts"]=results[:4]
	return render(request,"caeser.html",context)


############################################################

@staff_member_required
def put_attendance(request,lesson):
	context = {}
	context["lesson"] = Lesson.objects.get(id=lesson)
	context["students"] = Stream.objects.get(id=context["lesson"].stream.id).students.all().filter(profile__ended__isnull=True)
	if request.POST:
		if "absent" in request.POST:
			absent = request.POST["absent"].split(",")
			for student in context["students"]:
				if student.username in absent:
					if Attendance.objects.filter(user=student,lesson=context["lesson"]).exists():
						attended = Attendance.objects.get(user=student,lesson=context["lesson"])
						attended.attended = False
						attended.save()
					else:
						Attendance.objects.get_or_create(user=student,lesson=context["lesson"],attended=False)
				else:
					if Attendance.objects.filter(user=student,lesson=context["lesson"]).exists():
						attended = Attendance.objects.get(user=student,lesson=context["lesson"])
						attended.attended = True
						attended.save()
					else:
						Attendance.objects.create(user=student,lesson=context["lesson"])
			return redirect("cabinet")
	return render(request,"put_attendance.html",context)