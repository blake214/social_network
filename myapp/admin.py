from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

class UserConnectionJunctionsInline(admin.TabularInline):
    model = UserConnectionJunctions
    fk_name = 'user'
    extra = 3

class UserThreadJunctionsInline(admin.TabularInline):
    model = UserThreadJunctions
    extra = 3

class ThreadMessagesInline(admin.TabularInline):
    model = ThreadMessages
    extra = 3

class UserGalleriesInline(admin.TabularInline):
    model = UserGalleries
    extra = 3

class UserStatusesInline(admin.TabularInline):
    model = UserStatuses
    extra = 3

class UserDetailsInline(admin.StackedInline):
    model = UserDetails
    can_delete = False

class UserAdmin(UserAdmin):
    inlines = [UserDetailsInline, UserConnectionJunctionsInline, UserThreadJunctionsInline, UserGalleriesInline, UserStatusesInline]

class ThreadsAdmin(admin.ModelAdmin):
    inlines = [UserThreadJunctionsInline, ThreadMessagesInline]

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register the models
admin.site.register(User, UserAdmin)
admin.site.register(Threads, ThreadsAdmin)
admin.site.register(UserDetails)
admin.site.register(UserGalleries)
admin.site.register(UserStatuses)
admin.site.register(ThreadMessages)
admin.site.register(UserConnectionJunctions)
admin.site.register(UserThreadJunctions)