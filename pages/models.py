from django.db import models

FORWHOME_CHOICE = {
	('S', 'Работникам'),
    ('U', 'Ученикам'),
    ('B', 'Всем'),
}
# Create your models here.
class Manual(models.Model):
    forwhome = models.CharField(max_length=3,choices=FORWHOME_CHOICE,default='B',null=True,blank=True)
    question = models.CharField(max_length=255)
    answer = models.TextField(max_length=2000)