from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
	title = models.CharField(max_length=50,blank=False)
	user = models.ForeignKey(User)
	content = models.TextField(blank=False)
	created = models.DateTimeField(default=datetime.now)
	visible = models.BooleanField(default=True)

	def __str__(self):
		return str(self.title)

	class Meta:
		verbose_name = 'Объявление'
		verbose_name_plural = 'Объявления'