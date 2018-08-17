from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Activate, Reset, Helpful

class UserProfileInline(admin.StackedInline):
    model = Profile
  
class UserAdmin(DjangoUserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class ActivateAdmin(admin.ModelAdmin):
    model = Activate
    list_display = ('user','hash','assigned_date')
    search_fields=['user__first_name','user__last_name']

admin.site.register(Activate, ActivateAdmin)

class ResetAdmin(admin.ModelAdmin):
    model = Reset
    list_display = ('user','hash','assigned_date')
    search_fields=['user__first_name','user__last_name']
admin.site.register(Reset, ResetAdmin)

class HelpfulAdmin(admin.ModelAdmin):
    model = Helpful
    list_display = ('relation','name','helpful','contact')
    list_filter=['helpful']
    search_fields=['relation','name','helpful','comment','contact']
admin.site.register(Helpful, HelpfulAdmin)