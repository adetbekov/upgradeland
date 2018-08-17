from django.db import models

COLOR_CHOICE={
    ('D', 'Красный'),
    ('S', 'Зеленый'),
    ('W', 'Жёлтый'),
    ('I', 'Голубой'),
    ('P', 'Синий'),
}

class Event(models.Model):
	title = models.CharField(max_length=50)
	description = models.TextField(blank=True)
	date = models.DateTimeField()
	color = models.CharField(max_length = 1,choices=COLOR_CHOICE,default='P')
	visible = models.BooleanField(default=True)
	class Meta:
		verbose_name = "Событие"
		verbose_name_plural = "События"

	def __str__(self):
		return self.title
	