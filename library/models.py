from django.db import models
from datetime import datetime
from transliterate import translit

FILES_CHOICE={
	('F', 'Файл'),
	('P', 'PDF'),
	('D', 'Документ'),
	('V', 'Видео'),
	('A', 'Аудио'),
	('I', 'Изображения'),
	('Z', 'Архив'),
	('E', 'Excel'),
}

def upload_location(instance,filename):
	return "%s/%s" %('files',translit(filename,'ru',reversed=True))

# Create your models here.
class Shelf(models.Model):
	title = models.CharField(max_length=50)
	description = models.TextField(blank=True)
	created = models.DateTimeField(default=datetime.now)
	hidden = models.BooleanField(default=False)

	class Meta:
		verbose_name = "Полка"
		verbose_name_plural = "Полки"

	def __str__(self):
		return self.title

class Book(models.Model):
	shelf = models.ForeignKey(Shelf)
	name = models.CharField(max_length=255)
	typeof = models.CharField(max_length = 2,choices=FILES_CHOICE,default='F')
	image = models.ImageField(null=True,blank=True,upload_to=upload_location,)
	description = models.CharField(max_length=1000,blank=True,null=True)
	file = models.FileField(upload_to=upload_location,)
	created = models.DateTimeField(default=datetime.now)
	hidden = models.BooleanField(default=False)

	class Meta:
		verbose_name = "Материал"
		verbose_name_plural = "Материалы"

	def __str__(self):
		return str(self.name) + " - " + str(self.shelf)
	