from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime

class Plan(models.Model):
	title = models.CharField(max_length=50, blank=False)
	user = models.ForeignKey(User, blank=False)
	viewer = models.ManyToManyField(User,limit_choices_to={'is_staff': False}, related_name="viewers",blank=True)
	created = models.DateTimeField(default=datetime.now)
	ended = models.DateTimeField(blank=True, null=True)
	class Meta:
		verbose_name = "Чеклист"
		verbose_name_plural = "Чеклисты"

	def __str__(self):
		return str(self.title)+" "+str(self.user.username)
	

class MyTask(models.Model):
	plan = models.ForeignKey(Plan, blank=False)
	user = models.ForeignKey(User, blank=False)
	title = models.CharField(max_length=50, blank=False)
	created = models.DateTimeField(default=datetime.now)
	first = models.BooleanField(default=False)
	second = models.BooleanField(default=False)

	def __str__(self):
		return str(self.title)+" "+str(self.user.username)

	class Meta:
		verbose_name = 'План'
		verbose_name_plural = 'Планы'
