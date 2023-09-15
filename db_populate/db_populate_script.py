import os
import sys
import django
import csv
from collections import defaultdict
from django.utils import timezone
import datetime

sys.path.append("../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE','social_network.settings')
django.setup()

from myapp.models import *

# Datasets
auth_user = './auth_user.csv'
myapp_thread_messages = './myapp_thread_messages.csv'
myapp_threads = './myapp_threads.csv'
myapp_user_connection_junctions = './myapp_user_connection_junctions.csv'
myapp_user_details = './myapp_user_details.csv'
myapp_user_statuses = './myapp_user_statuses.csv'
myapp_user_thread_junctions = './myapp_user_thread_junctions.csv'

# Datastructures
users = defaultdict(list)
thread_messages = defaultdict(list)
threads = defaultdict(list)
user_connection_junctions = defaultdict(list)
user_details = defaultdict(list)
user_statuses = defaultdict(list)
user_thread_junctions = defaultdict(list)

# I wrote this code -------------------------- Start

# Just getting a valid time stamp
aware_datetime = timezone.now()
naive_datetime = datetime.datetime(2023, 8, 10, 16, 33, 47, 68000)
aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())

# Organise the data
with open(auth_user) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        user = defaultdict(dict)
        user['id'] = row[0]
        user['username'] = row[1]
        user['password'] = row[2]
        user['first_name'] = row[3]
        user['last_name'] = row[4]
        user['email'] = row[5]
        user['is_staff'] = row[6]
        user['is_active'] = row[7]
        user['date_joined'] = aware_datetime
        user['last_login'] = aware_datetime
        user['is_superuser'] = row[10]
        users[row[0]] = user

with open(myapp_thread_messages) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        thread_message = defaultdict(dict)
        thread_message['id'] = row[0]
        thread_message['thread'] = row[1]
        thread_message['creating_user'] = row[2]
        thread_message['message'] = row[3]
        thread_message['date_created'] = aware_datetime
        thread_messages[row[0]] = thread_message

with open(myapp_threads) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        thread = defaultdict(dict)
        thread['id'] = row[0]
        thread['title'] = row[1]
        thread['creating_user'] = row[2]
        thread['date_created'] = aware_datetime
        threads[row[0]] = thread

with open(myapp_user_connection_junctions) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        user_connection_junction = defaultdict(dict)
        user_connection_junction['id'] = row[0]
        user_connection_junction['user'] = row[1]
        user_connection_junction['user_connection'] = row[2]
        user_connection_junctions[row[0]] = user_connection_junction

with open(myapp_user_details) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        user_detail = defaultdict(dict)
        user_detail['user'] = row[0]
        user_detail['profile_image'] = row[1]
        user_detail['profile_image_thumb'] = row[2]
        user_detail['about_me'] = row[3]
        user_detail['date_created'] = aware_datetime
        user_details[row[0]] = user_detail

with open(myapp_user_statuses) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        user_status = defaultdict(dict)
        user_status['id'] = row[0]
        user_status['user'] = row[1]
        user_status['status'] = row[2]
        user_status['date_created'] = aware_datetime
        user_statuses[row[0]] = user_status

with open(myapp_user_thread_junctions) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        user_thread_junction = defaultdict(dict)
        user_thread_junction['id'] = row[0]
        user_thread_junction['user'] = row[1]
        user_thread_junction['thread'] = row[2]
        user_thread_junctions[row[0]] = user_thread_junction

# Keep track of records
user_records = {}
user_records_populator = []

thread_message_records = {}
thread_message_populator = []

thread_records = {}
thread_populator = []

user_connection_junction_records = {}
user_connection_junction_populator = []

user_detail_records = {}
user_detail_records_populator = []

user_status_records = {}
user_status_populator = []

user_thread_junction_records = {}
user_thread_junction_populator = []

# Populating DB
# Users
for key, user in users.items():
    row = User(**user)
    user_records[key] = row
    user_records_populator.append(row)
User.objects.bulk_create(user_records_populator)

# User_details
for key, user_detail in user_details.items():
    row = UserDetails(
        user = user_records[user_detail['user']],
        profile_image = user_detail['profile_image'],
        profile_image_thumb = user_detail['profile_image_thumb'],
        about_me = user_detail['about_me'],
        date_created = aware_datetime)
    user_detail_records[key] = row
    user_detail_records_populator.append(row)
UserDetails.objects.bulk_create(user_detail_records_populator)

# thread
for key, thread in threads.items():
    row = Threads(
        id = thread['id'],
        title = thread['title'],
        creating_user = user_records[thread['creating_user']],
        date_created = aware_datetime)
    thread_records[key] = row
    thread_populator.append(row)
Threads.objects.bulk_create(thread_populator)

# user_connection_junctions
for key, user_connection_junction in user_connection_junctions.items():
    row = UserConnectionJunctions(
        id = user_connection_junction['id'],
        user = user_records[user_connection_junction['user']],
        user_connection = user_records[user_connection_junction['user_connection']])
    user_connection_junction_records[key] = row
    user_connection_junction_populator.append(row)
UserConnectionJunctions.objects.bulk_create(user_connection_junction_populator)

# thread_message
for key, thread_message in thread_messages.items():
    row = ThreadMessages(
        id = thread_message['id'],
        thread = thread_records[thread_message['thread']],
        creating_user = user_records[thread_message['creating_user']],
        message = thread_message['message'],
        date_created = aware_datetime)
    thread_message_records[key] = row
    thread_message_populator.append(row)
ThreadMessages.objects.bulk_create(thread_message_populator)

# user_status
for key, user_status in user_statuses.items():
    row = UserStatuses(
        id = user_status['id'],
        user = user_records[user_status['user']],
        status = user_status['status'],
        date_created = aware_datetime)
    user_status_records[key] = row
    user_status_populator.append(row)
UserStatuses.objects.bulk_create(user_status_populator)

# user_thread_junctions
for key, user_thread_junction in user_thread_junctions.items():
    row = UserThreadJunctions(
        id = user_thread_junction['id'],
        user = user_records[user_thread_junction['user']],
        thread = thread_records[user_thread_junction['thread']])
    user_thread_junction_records[key] = row
    user_thread_junction_populator.append(row)
UserThreadJunctions.objects.bulk_create(user_thread_junction_populator)

# I wrote this code -------------------------- End