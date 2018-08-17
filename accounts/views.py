from .forms import RegUserForm, RegProfileForm, ActivateProfileForm, ActivateUserForm 
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import Activate, ActivateHelpfulForm, EditProfileForm, EditUserForm
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Helpful, Profile
from cabinet.models import Stream, Attendance
from datetime import datetime
from django_ajax.decorators import ajax
from functools import reduce
import operator
from django.db.models import Q

def logout(request):
	auth.logout(request)
	return redirect('index')

def login(request):
	if request.POST:
		username = request.POST["username"].lower().replace(" ","")
		password = request.POST["password"]
		user = auth.authenticate(username=username, password=password)
		if Activate.objects.filter(user__username=username).exists():
			activate = Activate.objects.filter(user__username=username)[0]
			if user is not None:
				return redirect("activate",activate.hash)
			else:
				context={}
				context['error']=True
				if 'next' in request.POST:
					context['next']=request.POST['next']
				return render(request,"index.html",context)
		elif user is not None and user.is_active:
			auth.login(request, user)
			if 'next' in request.POST:
				return HttpResponseRedirect(request.POST['next'])
			else:
				return redirect("feed")
		else:
			context={}
			context['error']=True
			if 'next' in request.POST:
				context['next']=request.POST['next']
			return render(request,"index.html",context)
	else:
		return render(request,"index.html")
	return render(request,"index.html")

@staff_member_required
def registration(request):
	context = {}
	form = RegUserForm(request.POST or None)
	profile = RegProfileForm(request.POST or None)
	context['form'] = form
	context['profile'] = profile
	if request.POST:
		if form.is_valid() and profile.is_valid():
			a = form.save()
			b = profile.save(commit=False)
			b.user = a
			b.save()
			user = User.objects.get(username=a)
			stream = Stream.objects.filter(finished__isnull=True).order_by("-name")
			if profile.cleaned_data.get('face') == "A":
				user.is_superuser=True
				user.is_staff=True
			elif profile.cleaned_data.get('face') == "T":
				user.is_staff=True
			else:
				if stream.exists():
					stream.last().students.add(user)
			user.save()
			return redirect("reg")
	return render(request,"registration.html",context)

def activate(request,hash):
	context = {}
	activate = Activate.objects.filter(hash = hash)
	if activate.exists():
		activate=activate[0]
		user=activate.user
		context["activate"] = activate
		if user.profile.helpful:
			if len(Helpful.objects.filter(relation=user))<5:
				form = ActivateHelpfulForm(request.POST or None)
				context['count'] = Helpful.objects.filter(relation=user).count()
				context['helpful'] = form
				if request.POST:
					if form.is_valid():
						b = form.save(commit=False)
						b.relation = user
						b.save()
						return redirect('activate',hash=activate.hash)
			else:
				activate.delete()
				return redirect('feed')
		else:
			form = ActivateUserForm(request.POST or None)
			profile = ActivateProfileForm(request.POST or None, instance = user.profile)
			context['form'] = form
			context['profile'] = profile
			if request.POST:
				if form.is_valid() and profile.is_valid():
					user.set_password(form.cleaned_data.get('password'))
					user.is_active=True
					user.save()
					profile.save()
					return redirect('activate',hash=activate.hash)
				else:
					context["error"]=True
	else:
		context["error"] = True
	return render(request,"activate.html",context)

@login_required
def profile(request, user_id):
	context = {}
	context["id"] = user_id
	context["user"] = None
	user = User.objects.filter(id = user_id)
	if user.exists():
		context["user"] = user[0]
		context["streams"] = Stream.objects.filter(students=user[0])
		context["contacts"] = Helpful.objects.filter(relation=user[0])
	return render(request,"profile.html",context)

@staff_member_required
def endcourse(request, user_id):
	profile = Profile.objects.get(user__id=user_id)
	profile.ended = datetime.now()
	profile.save()
	return redirect("profile",user_id)

@staff_member_required
def delete(request, user_id):
	profile = Profile.objects.get(user__id=user_id)
	profile.ended = datetime.now()
	profile.save()
	user = User.objects.get(id=user_id)
	user.is_active = False
	user.save()
	return redirect("profile",user_id)

@staff_member_required
def reanimate(request, user_id):
	profile = Profile.objects.get(user__id=user_id)
	profile.ended = None
	profile.save()
	user = User.objects.get(id=user_id)
	user.is_active = True
	user.save()
	return redirect("profile",user_id)

@login_required
def edit(request):
	context = {}
	form = EditUserForm(request.POST or None, instance=request.user)
	profile = EditProfileForm(request.POST or None, instance=request.user.profile)
	context['form'] = form
	context['profile'] = profile
	context['user'] = request.user
	return render(request,"edit.html",context)

@login_required
def edited(request,saved=False):
	context = {}
	form = EditUserForm(request.POST or None, instance=request.user)
	profile = EditProfileForm(request.POST or None, instance=request.user.profile)
	context['form'] = form
	context['profile'] = profile
	context['user'] = request.user
	context['saved'] = saved
	return render(request,"edit.html",context)

@login_required
def editprofile(request):
	context = {}
	form = EditUserForm(request.POST or None, instance=request.user)
	profile = EditProfileForm(request.POST or None, request.FILES, instance=request.user.profile)
	context['form'] = form
	context['profile'] = profile
	context['user'] = request.user
	if request.POST:
		if profile.is_valid():
			profile.save()
			return redirect("edited",saved=True)
	return render(request,"edit.html",context)

@login_required
def edituser(request):
	context = {}
	form = EditUserForm(request.POST or None, instance=request.user)
	context['form'] = form
	context['user'] = request.user
	context['form_active'] = True
	if request.POST:
		if form.is_valid():
			form.save()
			return redirect("edited",saved=True)
	return render(request,"edit.html",context)

@staff_member_required
def all(request):
	context = {}
	return render(request,"all.html",context)

@ajax
def client_ajax(request):
	context={}
	if request.GET:
		q = request.GET.get('client')
		if q!=None and len(q)>2:
			queries = q.split()
			qset1 =  reduce(operator.__and__, [Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__iendswith=query)  for query in queries])
			results = User.objects.filter(qset1).distinct()
			context['users']=results
			context['client']=request.GET.get('client')
			if len(context['users'])==1:
				exact=context['users'][0]
				return {'exact':redirect("profile",exact.id),'full_name':exact.get_full_name()}
			else:
				exact=None
				return render(request,"client_ajax.html",context)