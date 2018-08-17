from django import forms
from django.forms import ModelForm, Textarea,SelectDateWidget, Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from .models import Profile, Activate, Reset, Helpful
from django.contrib.auth.models import User
from upgrade import functions
import re, datetime
from django.forms import formset_factory
from django.forms.extras import widgets

now = datetime.datetime.now()
BIRTH_YEAR_CHOICES = list()
# BIRTH_YEAR_CHOICES.append('')
for i in range(80):
	BIRTH_YEAR_CHOICES.append((now.year-5)-i)


widget=widgets.SelectDateWidget(
		years=BIRTH_YEAR_CHOICES)



class RegUserForm(ModelForm):
	class Meta:
		model = User
		fields = ('first_name','last_name', 'email')

	def clean_last_name(self):
		if len(self.cleaned_data.get('last_name'))!=0:
			lastname=self.cleaned_data.get('last_name').lower()
			lastname=lastname[0].upper()+lastname[1:]
			if len(lastname)<1:
				raise forms.ValidationError('Обязательное поле')
			return lastname
		else:
			raise forms.ValidationError('Обязательное поле')
	def clean_first_name(self):
		if len(self.cleaned_data.get('first_name'))!=0:
			firstname=self.cleaned_data.get('first_name').lower()
			firstname=firstname[0].upper()+firstname[1:]
			if len(firstname)<1 or firstname=="":
				raise forms.ValidationError('Обязательное поле')
			re.split(r'^[0-9_~!@#$%^&*()=+\.,/|[]{}''""><:;?]+$--', firstname)
			return firstname
		else:
			raise forms.ValidationError('Обязательное поле')
	def clean_email(self):
		email=self.cleaned_data.get('email')
		if len(email)<5:
			raise forms.ValidationError('Обязательное поле')
		return email

	def save(self, commit=True):
		pwstring = functions.randhash(8)
		user = super(RegUserForm, self).save(commit=False)
		user.set_password(pwstring)
		lname = functions.rutoen(str(self.cleaned_data.get('last_name')).lower())
		fname = functions.rutoen(str(self.cleaned_data.get('first_name')).lower())
		user.username=functions.strnormalize(lname+"_"+fname)
		user.is_active=False
		if commit:
			user.save()
			Activate.objects.create(user=user,hash=pwstring)
			functions.send_confirm_message(user,pwstring)
			return user

	def clean(self):
		cleaned_data = super(RegUserForm, self).clean()
		lname = functions.rutoen(str(self.cleaned_data.get('last_name')).lower())
		fname = functions.rutoen(str(self.cleaned_data.get('first_name')).lower())
		user = functions.strnormalize(lname+"_"+fname)
		if User.objects.filter(username=str(user)).exists():
			raise forms.ValidationError('Пользователь с таким логином уже существует!')

	helper = FormHelper()
	helper.layout = Layout(
		'first_name',
		'last_name',
		'email',
	)

class RegProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ('face',)
		widgets = {
			'face': forms.Select(),
		}

	helper = FormHelper()
	helper.layout = Layout(
		'face',
	)

class ActivateProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ["birth","phone","helpful","university"]
		labels = {
			'birth' : ('Дата рождения'),
			'phone' : ('Телефон'),
			'helpful' : ('Чем полезен'),
			'university' : ('ВУЗ'),
		}
		widgets = {
			'birth': widget,
		} 

	def clean_phone(self):
		phone = self.cleaned_data.get('phone')
		if len(phone)!=0:
			if len(phone)<11:
				raise forms.ValidationError('Обязательное поле')
		else:
			raise forms.ValidationError('Обязательное поле')
		return phone
	def clean_helpful(self):
		helpful = self.cleaned_data.get('helpful').lower()
		helpful = helpful[0].upper()+helpful[1:]
		if len(helpful)!=0:
			if len(helpful)<4:
				raise forms.ValidationError('Обязательное поле')
			if len(helpful.split(" "))>2:
				raise forms.ValidationError('Опишите двумя или одним словом!')
			if len(helpful)>140:
				raise forms.ValidationError('Опишите короче (140 симфолов)!')
		else:
			raise forms.ValidationError('Обязательное поле')
		return helpful
	def clean_university(self):
		university = self.cleaned_data.get('university')
		if len(university)!=0:
			if len(university)>20:
				raise forms.ValidationError('Лимит на символы исчерпан (20 символов)')
		else:
			raise forms.ValidationError('Обязательное поле')
		return university

	helper = FormHelper()
	helper.layout = Layout(
		'birth',
		'phone',
		'helpful',
		'university',
	)

class ActivateUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ["password"]
		# widgets = {
		# 	'password': forms.PasswordInput(),
		# } 

	def clean_password(self):
		phone = self.cleaned_data.get('password')
		if len(phone)!=0:
			if len(phone)<5:
				raise forms.ValidationError('Пароль должен состоять из не менее 5 символов')
		else:
			raise forms.ValidationError('Обязательное поле')
		return phone

	helper = FormHelper()
	helper.layout = Layout(
		'password',
	)

class ActivateHelpfulForm(forms.ModelForm):
	class Meta:
		model = Helpful
		fields = ["name","helpful","contact","comment"]
		labels = {
			'name' : ('Имя'),
			'helpful' : ('Чем полезен (профессия)'),
			'contact' : ('Номер телефона'),
			'comment' : ('Комментарий'),
		}
		widgets = {
			'comment': forms.Textarea(attrs={'rows':3}),
		} 
	def clean_contact(self):
		phone = self.cleaned_data.get('contact')
		if len(phone)!=0:
			if len(phone)<8:
				raise forms.ValidationError('Обязательное поле')
		else:
			raise forms.ValidationError('Обязательное поле')
		return phone
	def clean_helpful(self):
		helpful = self.cleaned_data.get('helpful').lower()
		helpful = helpful[0].upper()+helpful[1:]
		if len(helpful)!=0:
			if len(helpful)<4:
				raise forms.ValidationError('Обязательное поле')
			if len(helpful.split(" "))>2:
				raise forms.ValidationError('Опишите двумя или одним словом!')
			if len(helpful)>140:
				raise forms.ValidationError('Опишите короче (140 симфолов)!')
		else:
			raise forms.ValidationError('Обязательное поле')
		return helpful
	def clean_name(self):
		if Helpful.objects.filter(name__iexact=self.cleaned_data.get('name')):
			raise forms.ValidationError('Такой пользователь уже есть в базе!')
		if len(self.cleaned_data.get('name'))!=0:
			firstname=self.cleaned_data.get('name').lower()
			firstname=" ".join(str(i[0].upper()+i[1:]) for i in firstname.split(" "))
			if len(firstname)<2 or firstname=="":
				raise forms.ValidationError('Обязательное поле')
			re.split(r'^[0-9_~!@#$%^&*()=+\.,/|[]{}''""><:;?]+$--', firstname)
			return firstname
		else:
			raise forms.ValidationError('Обязательное поле')
	def clean_comment(self):
		email=self.cleaned_data.get('comment')
		if len(email)<5:
			raise forms.ValidationError('Ну напишите подробнее, пожалуйста!')
		return email
	helper = FormHelper()
	helper.layout = Layout(
		'name',
		'helpful',
		'contact',
		'comment',
	)	

class EditProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ["birth","phone","helpful","university","image"]
		labels = {
			'birth' : ('Дата рождения'),
			'image' : ('Фотка'),
			'phone' : ('Телефон'),
			'helpful' : ('Чем полезен'),
			'university' : ('ВУЗ'),
		}
		widgets = {
			'birth': widget,
		} 

	def clean_phone(self):
		phone = self.cleaned_data.get('phone')
		if len(phone)!=0:
			if len(phone)<11:
				raise forms.ValidationError('Обязательное поле')
		else:
			raise forms.ValidationError('Обязательное поле')
		return phone
	def clean_helpful(self):
		helpful = self.cleaned_data.get('helpful').lower()
		helpful = helpful[0].upper()+helpful[1:]
		if len(helpful)!=0:
			if len(helpful)<4:
				raise forms.ValidationError('Обязательное поле')
			if len(helpful.split(" "))>2:
				raise forms.ValidationError('Опишите двумя или одним словом!')
			if len(helpful)>140:
				raise forms.ValidationError('Опишите короче (140 симфолов)!')
		else:
			raise forms.ValidationError('Обязательное поле')
		return helpful
	def clean_university(self):
		university = self.cleaned_data.get('university')
		if len(university)!=0:
			if len(university)>140:
				raise forms.ValidationError('Лимит на символы исчерпан (140 символов)')
		else:
			raise forms.ValidationError('Обязательное поле')
		return university

	helper = FormHelper()
	helper.layout = Layout(
		'birth',
		'phone',
		'helpful',
		'university',
		'image',
	)

class EditUserForm(forms.ModelForm):
	old_password = forms.CharField(required=False,label='Старый пароль',widget=forms.TextInput(attrs={'placeholder': 'Не обязательно если вы меняете email'}))
	password = forms.CharField(required=False,label='Новый пароль',widget=forms.TextInput(attrs={'placeholder': 'Не обязательно если вы меняете email'}))
	class Meta:
		model = User
		fields = ["email"]
	def clean_email(self):
		email=self.cleaned_data.get('email')
		if email != "":
			if len(email)<5:
				raise forms.ValidationError('Обязательное поле')
		else:
			raise forms.ValidationError('Обязательное поле')
		return email
	def clean_password(self):
		phone = self.cleaned_data.get('password')
		if len(phone)!=0 and len(phone)<5:
				raise forms.ValidationError('Пароль должен состоять из не менее 5 символов')
		return phone
	def clean_old_password(self):
		phone = self.cleaned_data.get('old_password')
		if len(phone)!=0 and len(phone)<5:
				raise forms.ValidationError('Пароль должен состоять из не менее 5 символов')
		return phone
	def clean(self):
		user = User.objects.get(username = self.instance)
		password = self.cleaned_data.get('password')
		old_password = self.cleaned_data.get('old_password')
		if password!=None and old_password==None:
			raise forms.ValidationError('Введите старый пароль!')
		if password==None and old_password!=None:
			raise forms.ValidationError('Введите новый пароль!')
		if password!="" or old_password!="":
			if not user.check_password(old_password):
				raise forms.ValidationError('Старый пароль неверный!')
			else:
				if password=="":
					raise forms.ValidationError('Введите новый пароль!')
				if password==old_password:
					raise forms.ValidationError('Новый пароль должен отличаться от старого!')
	def save(self, commit=True):
		user = super(EditUserForm, self).save(commit=False)
		u = self.instance
		password = self.cleaned_data.get('password')
		old_password = self.cleaned_data.get('old_password')
		if password!=old_password and password!="" and old_password!="":
			if user.check_password(old_password):
				user.set_password(password)
		user.email = self.cleaned_data.get('email')
		if commit:
			user.save()
			return user
	helper = FormHelper()
	helper.layout = Layout(
		'old_password'
		'password',
		'email',
	)