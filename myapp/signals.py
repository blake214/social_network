from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *

# I wrote this code -------------------------- Start
@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    '''create_user_details
    A signal reciever for when a 'user' record is created. Will create a record in the 'user_details' table to match.

    sender = Model Class: the class that sends the signal
    instance = Model Class Instance: an instance of the User model record created
    created = Boolean: stating if 'user' record has been created

    returns: Nothing
    '''
    if created:
        UserDetails.objects.create(**{'user': instance})
# I wrote this code -------------------------- End