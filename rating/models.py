from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Rate(models.Model):
	title = models.CharField(blank=True,max_length=50)
	created = models.DateTimeField(default=datetime.now)
	visible = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Рейтинг"
		verbose_name_plural = "Рейтинги"

	def __str__(self):
		return str(self.title) + " - " + str(self.created)

class Top(models.Model):
	ratelist = models.ForeignKey(Rate)
	student = models.ManyToManyField(User,limit_choices_to={'is_staff': False})
	comment = models.TextField(blank=True)
	place = models.IntegerField()
	visible = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Топ студент"
		verbose_name_plural = "Топ студенты"	

