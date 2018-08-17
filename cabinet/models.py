from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from redactor.fields import RedactorField
from transliterate import translit


def upload_location(instance, filename):
    return "%s/%s" % ('video', translit(filename, 'ru', reversed=True))


# Create your models here.
class Stream(models.Model):
    name = models.CharField(max_length=20, blank=False)
    description = models.TextField(blank=True)
    students = models.ManyToManyField(User, limit_choices_to={'is_staff': False}, related_name="participants",
                                      blank=True)
    created = models.DateTimeField(default=datetime.now)
    finished = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Поток'
        verbose_name_plural = 'Потоки'


def stream():
    return Stream.objects.all().order_by("pk")[0]


class Lesson(models.Model):
    stream = models.ForeignKey(Stream, blank=False, default=stream)
    name = models.CharField(max_length=30, blank=False)
    day = models.DateField(blank=False, null=False)
    place = models.CharField(max_length=30, blank=True)
    tutor = models.ForeignKey(User, limit_choices_to={'is_staff': True}, blank=False)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=upload_location, blank=True, null=True)
    content = RedactorField(verbose_name=u'Текст', upload_to='lessons/content/', allow_file_upload=True,
                            allow_image_upload=True, blank=True)
    hw = RedactorField(verbose_name=u'Домашнее задание', upload_to='lessons/hw/', allow_file_upload=True,
                       allow_image_upload=True, blank=True)
    created = models.DateTimeField(default=datetime.now)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name) + " " + str(self.stream)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Attendance(models.Model):
    lesson = models.ForeignKey(Lesson, blank=False)
    user = models.ForeignKey(User, blank=False)
    attended = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.user) + " " + str(self.lesson)

    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'


class HomeTask(models.Model):
    lesson = models.ForeignKey(Lesson, blank=False)
    name = models.CharField(max_length=50, blank=False)
    created = models.DateTimeField(default=datetime.now)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name) + " " + str(self.lesson)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'


class CheckedTask(models.Model):
    task = models.ForeignKey(HomeTask)
    user = models.ForeignKey(User, blank=False)
    created = models.DateTimeField(default=datetime.now)
    second = models.BooleanField(default=False)

    def __str__(self):
        return str(self.task) + " " + str(self.user)

    class Meta:
        verbose_name = 'Выполненное задание'
        verbose_name_plural = 'Выполненные задания'
