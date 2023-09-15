from django.db import models
from django.contrib.auth.models import User

# I wrote this code -------------------------- Start
class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='UserDetails')
    profile_image = models.FileField(blank=True, null=True)
    profile_image_thumb = models.FileField(blank=True, null=True)
    about_me = models.CharField(max_length=256, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'myapp_user_details'

    def __str__(self):
        return self.user.username
    
class UserGalleries(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserGalleries')
    gallery_image = models.FileField(blank=False, null=False)
    gallery_image_thumb = models.FileField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'myapp_user_galleries'

    def __str__(self):
        return self.id

class UserStatuses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserStatuses')
    status = models.CharField(max_length=256, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'myapp_user_statuses'

    def __str__(self):
        return self.status

class Threads(models.Model):
    title = models.CharField(max_length=256, null=False, blank=False)
    creating_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='Threads_creating_user')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'myapp_threads'

    def __str__(self):
        return str(self.id)

class ThreadMessages(models.Model):
    thread = models.ForeignKey(Threads, on_delete=models.CASCADE, related_name='ThreadMessages')
    creating_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='ThreadMessages')
    message = models.CharField(max_length=256, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'myapp_thread_messages'

    def __str__(self):
        return str(self.id)

class UserConnectionJunctions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserConnectionsJunction_user')
    user_connection = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserConnectionsJunction_user_connection')

    class Meta:
        unique_together = ('user', 'user_connection')
        db_table = 'myapp_user_connection_junctions'

class UserThreadJunctions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserThreadsJunction')
    thread = models.ForeignKey(Threads, on_delete=models.CASCADE, related_name='UserThreadsJunction')

    class Meta:
        unique_together = ('user', 'thread')
        db_table = 'myapp_user_thread_junctions'
# I wrote this code -------------------------- End