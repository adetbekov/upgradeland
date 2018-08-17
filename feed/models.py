from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
def upload_location(instance,filename):
    return "posts/%s/%s" %(instance.id,filename)

class Post(models.Model):
	user = models.ForeignKey(User)
	content = models.TextField()
	image = models.ImageField(null=True,blank=True,upload_to=upload_location)
	visible = models.BooleanField(default=True)
	created = models.DateTimeField(default=datetime.now())

	class Meta:
		verbose_name = "Пост"
		verbose_name_plural = "Посты"

	def __str__(this):
		return str(this.user) + " - " + str(this.id) + " - post" 
class PostLike(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	created = models.DateTimeField(default=datetime.now())

	class Meta:
		verbose_name = "Лайк поста"
		verbose_name_plural = "Лайки постов"

	def __str__(this):
		return str(this.post) + " - like" 

class PostComment(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	comment = models.TextField()
	visible = models.BooleanField(default=True)
	created = models.DateTimeField(default=datetime.now())

	class Meta:
		verbose_name = "Коммент поста"
		verbose_name_plural = "Комменты постов"

	def __str__(this):
		return str(this.post) + " - comment" 