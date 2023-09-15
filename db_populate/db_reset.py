import os
import sys
import django

sys.path.append("../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE','social_network.settings')
django.setup()

from myapp.models import *

# I wrote this code -------------------------- Start

# Clean DB
UserDetails.objects.all().delete()
ThreadMessages.objects.all().delete()
Threads.objects.all().delete()
UserConnectionJunctions.objects.all().delete()
UserThreadJunctions.objects.all().delete()
UserStatuses.objects.all().delete()
User.objects.all().delete()

# I wrote this code -------------------------- End