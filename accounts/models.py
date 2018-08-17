from django.db import models
from django.contrib.auth.models import User

FACE_CHOICE={
    ('OS', 'Online Student'),
    ('GS', 'General Student'),
    ('T', 'Teacher'),
    ('A', 'Admin'),
}
# Create your models here.
def upload_location(instance,filename):
    return "%s/%s" %(instance.id,filename)

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    birth=models.DateField(null=True)
    phone=models.CharField(max_length = 12,null=True)
    helpful=models.CharField(max_length = 140,null=True)
    university=models.CharField(max_length = 30,null=True)
    face = models.CharField(max_length = 3,choices=FACE_CHOICE,default='OS')
    image=models.ImageField(null=True,blank=True,
                            upload_to=upload_location,
                            height_field="height_field",
                            width_field="width_field",)
    height_field = models.IntegerField(default=0,null=True,blank=True)
    width_field = models.IntegerField(default=0,null=True,blank=True)
    ended = models.DateField(null=True,blank=True)

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])

class Activate(models.Model):
    user=models.OneToOneField(User)
    hash=models.CharField(max_length=255)
    assigned_date=models.DateField(auto_now=False,auto_now_add=True)

    class Meta:
        verbose_name = 'Активация'
        verbose_name_plural = 'Активации'

class Helpful(models.Model):
    relation = models.ForeignKey(User, blank=True,null=True)
    name = models.CharField(max_length=50, blank=False,null=False)
    helpful=models.CharField(max_length = 140)
    contact=models.CharField(max_length = 140)
    comment=models.TextField()

    class Meta:
        verbose_name = "Полезный контакт"
        verbose_name_plural = "Полезные контакты"

    def __str__(self):
        return str(self.name)
    

class Reset(models.Model):
    user=models.OneToOneField(User)
    hash=models.CharField(max_length=255)
    assigned_date=models.DateField(auto_now=False,auto_now_add=True)

    class Meta:
        verbose_name = 'Восстановление пароля'
        verbose_name_plural = 'Восстановления паролей'