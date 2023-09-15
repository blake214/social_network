import factory
from faker import Faker
from .models import *

# I wrote this code -------------------------- Start
class UserFactory(factory.django.DjangoModelFactory):
    first_name = Faker().first_name()
    last_name = Faker().last_name()
    username = factory.Sequence(lambda n: "username_%03d" % n) 
    email = Faker().email()
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = User

class UserDetailsFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    profile_image = factory.django.ImageField()
    profile_image_thumb = factory.django.ImageField()
    about_me = factory.Faker('text', max_nb_chars=256) 

    class Meta:
        model = UserDetails

class UserGalleriesFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    gallery_image = factory.django.ImageField()
    gallery_image_thumb = factory.django.ImageField()

    class Meta:
        model = UserGalleries

class UserStatusesFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    status = factory.Faker('text', max_nb_chars=256) 

    class Meta:
        model = UserStatuses

class ThreadsFactory(factory.django.DjangoModelFactory):
    creating_user = factory.SubFactory(UserFactory)
    title = factory.Faker('text', max_nb_chars=100) 

    class Meta:
        model = Threads

class ThreadMessagesFactory(factory.django.DjangoModelFactory):
    thread = factory.SubFactory(ThreadsFactory)
    creating_user = factory.SubFactory(UserFactory)
    message = factory.Faker('text', max_nb_chars=500) 

    class Meta:
        model = ThreadMessages

class UserConnectionJunctionsFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    user_connection = factory.SubFactory(UserFactory)

    class Meta:
        model = UserConnectionJunctions

class UserThreadJunctionsFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    thread = factory.SubFactory(ThreadsFactory)

    class Meta:
        model = UserThreadJunctions
# I wrote this code -------------------------- End