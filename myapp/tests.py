from django.urls import reverse
from rest_framework.test import APITestCase
from django.db import transaction

from .signals import *
from .api import *
from .model_factories import *

'''
NOTE: 
If you get an atomic error, i think this is due to the signals handler for when creating the users, it creates the user_details. 
So some times it might pop this error as might still be busy with the handler when the tests are run. Not sure how to prevent this and also test the signals
'''

# I wrote this code -------------------------- Start
class UserLoginTest(APITestCase):
    ''' Test for 'login' 
    '''
    user_1 = None
    user_2 = None

    def setUp(self):
        ''' Setup for the test case
        Initialises the temp database with some data
        '''
        self.user_1 = UserFactory.create(username="username_1",password="password")
        self.user_2 = UserFactory.create(username="username_2", password="password")

    def tearDown(self):
        ''' Cleanup any test data
        '''
        UserDetails.objects.all().delete()
        UserGalleries.objects.all().delete()
        UserStatuses.objects.all().delete()
        Threads.objects.all().delete()
        ThreadMessages.objects.all().delete()
        UserConnectionJunctions.objects.all().delete()
        UserThreadJunctions.objects.all().delete()
        User.objects.all().delete()

    def test_userLoggedInLogout(self):
        ''' Test
        Test if the endpoint handels
        Login User
        '''
        # Logging the user in
        response = self.client.post(reverse('login'), {'username': 'username_1', 'password': 'password'})
        # Check if the response is successful: returns redirect status
        self.assertEqual(response.status_code, 302)
        # Check if the user is logged in
        self.assertTrue('_auth_user_id' in self.client.session)
        # Check if the user is logged in
        self.assertEqual(response.wsgi_request.user, self.user_1)

        # Logging the user out
        self.client.get(reverse('logout'))
        # Check if the user is logged in
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_userLoggedInIncorrectCredentials(self):
        ''' Test
        Test if the endpoint handels
        Login User With Incorrect Credentials
        '''
        # Logging the user in
        response = self.client.post(reverse('login'), {'username': 'username_1', 'password': 'wrongpassword'})
        # Check if the response is successful: returns client error status
        self.assertEqual(response.status_code, 400)
        # Check if the user is logged in
        self.assertFalse('_auth_user_id' in self.client.session)


class UpdateUserTest(APITestCase):
    ''' Test for 'update_user' 
    '''
    user_1 = None

    def setUp(self):
        ''' Setup for the test case
        Initialises the temp database with some data
        '''
        self.user_1 = UserFactory.create(username="username_1",password="password")

    def tearDown(self):
        ''' Cleanup any test data
        '''
        UserDetails.objects.all().delete()
        UserGalleries.objects.all().delete()
        UserStatuses.objects.all().delete()
        Threads.objects.all().delete()
        ThreadMessages.objects.all().delete()
        UserConnectionJunctions.objects.all().delete()
        UserThreadJunctions.objects.all().delete()
        User.objects.all().delete()

    def test_userChange(self):
        ''' Test
        Test if the endpoint handels
        Update user record
        '''
        # Logging the user in, and check logged in
        response = self.client.post(reverse('login'), {'username': 'username_1', 'password': 'password'})
        self.assertEqual(response.wsgi_request.user, self.user_1)

        # Setting up for the request
        csrf_token = self.client.cookies['csrftoken'].value
        headers = {'HTTP_X-CSRFToken': csrf_token}

        # Deleting a user_status: returns no content status
        data = {
            'username': self.user_1.username, 
            'email': 'worm@example.com', 
            'first_name': 'worm', 
            'last_name': 'worm', 
            'about_me': 'worm', 
            'csrfmiddlewaretoken': csrf_token
            }
        response = self.client.post(reverse('update_user'), data, **headers)
        self.assertEqual(response.status_code, 302)
        # Getting database records
        user = User.objects.get(username=self.user_1.username)
        user_details_record = UserDetails.objects.get(user=user)
        # Checking if records exist
        self.assertEqual(user.email, 'worm@example.com')
        self.assertEqual(user.first_name, 'worm')
        self.assertEqual(user.last_name, 'worm')
        self.assertEqual(user_details_record.about_me, 'worm')

class RegisterUserTest(APITestCase):
    ''' Test for 'register' 
    '''
    user_1 = None

    def setUp(self):
        ''' Setup for the test case
        Initialises the temp database with some data
        '''
        self.user_1 = UserFactory.create(username="username_1",password="password")

    def tearDown(self):
        ''' Cleanup any test data
        '''
        UserDetails.objects.all().delete()
        UserGalleries.objects.all().delete()
        UserStatuses.objects.all().delete()
        Threads.objects.all().delete()
        ThreadMessages.objects.all().delete()
        UserConnectionJunctions.objects.all().delete()
        UserThreadJunctions.objects.all().delete()
        User.objects.all().delete()

    @transaction.atomic
    def test_registerUser(self):
        ''' Test
        Test if the endpoint handels
        Create & Create Duplicate
        '''
        # Creating a user: returns redirect status
        data = {
            'username': 'username_2', 
            'email': 'username_2@example.com', 
            'first_name': 'user', 
            'last_name': 'name', 
            'password1': 'password',
            'password2': 'password',
            }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        # Getting database records
        user = User.objects.get(username='username_2')
        user_details_record = UserDetails.objects.get(user=user)
        # Checking if records exist
        self.assertIsInstance(user, User)
        self.assertIsInstance(user_details_record, UserDetails)

        # Creating a duplicate user: returns client created error
        data = {
            'username': self.user_1.username, 
            'email': 'username_1@example.com', 
            'first_name': 'user', 
            'last_name': 'name', 
            'password1': 'password',
            'password2': 'password',
            }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 400)


class UserSearchTest(APITestCase):
    ''' Test for 'user_search_api' 
    '''
    user_1 = None
    user_2 = None

    def setUp(self):
        ''' Setup for the test case
        Initialises the temp database with some data
        '''
        self.user_1 = UserFactory.create(username="username_1",password="password")
        self.user_2 = UserFactory.create(username="username_2",password="password")

    def tearDown(self):
        ''' Cleanup any test data
        '''
        UserDetails.objects.all().delete()
        UserGalleries.objects.all().delete()
        UserStatuses.objects.all().delete()
        Threads.objects.all().delete()
        ThreadMessages.objects.all().delete()
        UserConnectionJunctions.objects.all().delete()
        UserThreadJunctions.objects.all().delete()
        User.objects.all().delete()

    def test_recieveRecords(self):
        ''' Test
        Test if the endpoint handels
        Quering the database and recieving the correct data
        '''
        # Logging the user in, and check logged in
        response = self.client.post(reverse('login'), {'username': 'username_1', 'password': 'password'})
        self.assertEqual(response.wsgi_request.user, self.user_1)

        # Setting up for the request
        csrf_token = self.client.cookies['csrftoken'].value
        headers = {'HTTP_X-CSRFToken': csrf_token}

        # Searching to recieve one record
        response = self.client.get(reverse('user_search_api') + f'?search=username_1', **headers)
        self.assertEqual(response.data[0].get('username'), 'username_1')
        self.assertEqual(len(response.data), 1)

        # Searching to recieve two record
        response = self.client.get(reverse('user_search_api') + f'?search=username_', **headers)
        self.assertEqual(len(response.data), 2)


class UserStatusTest(APITestCase):
    ''' Test for 'user_status_api' 
    '''
    user_1 = None
    status = None

    def setUp(self):
        ''' Setup for the test case
        Initialises the temp database with some data
        '''
        self.user_1 = UserFactory.create(username="username_1",password="password")
        self.status = UserStatusesFactory.create(user=self.user_1, status="status")

    def tearDown(self):
        ''' Cleanup any test data
        '''
        UserDetails.objects.all().delete()
        UserGalleries.objects.all().delete()
        UserStatuses.objects.all().delete()
        Threads.objects.all().delete()
        ThreadMessages.objects.all().delete()
        UserConnectionJunctions.objects.all().delete()
        UserThreadJunctions.objects.all().delete()
        User.objects.all().delete()

    def test_userStatusCreate(self):
        ''' Test
        Test if the endpoint handels
        Create
        '''
        # Logging the user in, and check logged in
        response = self.client.post(reverse('login'), {'username': 'username_1', 'password': 'password'})
        self.assertEqual(response.wsgi_request.user, self.user_1)

        # Setting up for the request
        csrf_token = self.client.cookies['csrftoken'].value
        headers = {'HTTP_X-CSRFToken': csrf_token}

        # Creating a user_connection_junction: returns created status
        data = {
            'title': 'status', 
            'csrfmiddlewaretoken': csrf_token
            }
        response = self.client.post(reverse('user_status_api'), data, **headers)
        self.assertEqual(response.status_code, 201)

    @transaction.atomic
    def test_userStatusDelete(self):
        ''' Test
        Test if the endpoint handels
        Delete & Delete Non Existing
        '''
        # Logging the user in, and check logged in
        response = self.client.post(reverse('login'), {'username': 'username_1', 'password': 'password'})
        self.assertEqual(response.wsgi_request.user, self.user_1)

        # Setting up for the request
        csrf_token = self.client.cookies['csrftoken'].value
        headers = {'HTTP_X-CSRFToken': csrf_token}

        # Deleting a user_status: returns no content status
        response = self.client.delete(reverse('user_status_api') + f'?status_id={self.status.id}', **headers)
        self.assertEqual(response.status_code, 204)

        # Deleting a user_status that doesnt exist: returns not found status
        headers = {'HTTP_X-CSRFToken': csrf_token}
        response = self.client.delete(reverse('user_status_api') + f'?status_id=10001', **headers)
        self.assertEqual(response.status_code, 404)

class UserConnectionsTest(APITestCase):
    ''' Test for 'user_connection_junction_api' 
    '''
    user_1 = None
    user_2 = None
    user_3 = None
    user_connection_1 = None

    def setUp(self):
        ''' Setup for the test case
        Initialises the temp database with some data
        '''
        self.user_1 = UserFactory.create(username="username_1",password="password")
        self.user_2 = UserFactory.create(username="username_2", password="password")
        self.user_3 = UserFactory.create(username="username_3", password="password")
        self.user_connection_1 = UserConnectionJunctionsFactory.create(user=self.user_1, user_connection= self.user_3)

    def tearDown(self):
        ''' Cleanup any test data
        '''
        UserDetails.objects.all().delete()
        UserGalleries.objects.all().delete()
        UserStatuses.objects.all().delete()
        Threads.objects.all().delete()
        ThreadMessages.objects.all().delete()
        UserConnectionJunctions.objects.all().delete()
        UserThreadJunctions.objects.all().delete()
        User.objects.all().delete()

    @transaction.atomic
    def test_userCreateConnection(self):
        ''' Test
        Test if the endpoint handels
        Create & Create Duplicate
        '''
        # Logging the user in, and check logged in
        response = self.client.post(reverse('login'), {'username': 'username_1', 'password': 'password'})
        self.assertEqual(response.wsgi_request.user, self.user_1)

        # Setting up for the request
        csrf_token = self.client.cookies['csrftoken'].value
        headers = {'HTTP_X-CSRFToken': csrf_token}

        # Creating a user_connection_junction: returns created status
        data = {
            'user_connection': self.user_2.id, 
            'csrfmiddlewaretoken': csrf_token
            }
        response = self.client.post(reverse('user_connection_junction_api'), data, **headers)
        self.assertEqual(response.status_code, 201)

        # Creating a duplicate user_connection_junction: returns client created error
        data = {
            'user_connection': self.user_3.id, 
            'csrfmiddlewaretoken': csrf_token
            }
        response = self.client.post(reverse('user_connection_junction_api'), data, **headers)
        self.assertEqual(response.status_code, 400)

    @transaction.atomic
    def test_userDeleteConnection(self):
        ''' Test
        Test if the endpoint handels
        Delete & Delete Non Existing
        '''
        # Logging the user in, and check logged in
        response = self.client.post(reverse('login'), {'username': 'username_1', 'password': 'password'})
        self.assertEqual(response.wsgi_request.user, self.user_1)

        # Setting up for the request
        csrf_token = self.client.cookies['csrftoken'].value
        headers = {'HTTP_X-CSRFToken': csrf_token}

        # Deleting a user_connection_junction: returns no content status
        response = self.client.delete(reverse('user_connection_junction_api') + f'?user_connection_id={self.user_3.id}', **headers)
        self.assertEqual(response.status_code, 204)

        # Deleting a user_connection_junction that doesnt exist: returns not found status
        headers = {'HTTP_X-CSRFToken': csrf_token}
        response = self.client.delete(reverse('user_connection_junction_api') + f'?user_connection_id=10001', **headers)
        self.assertEqual(response.status_code, 404)


class ThreadTest(APITestCase):
    ''' Test for 'thread_api' 
    '''
    user_1 = None
    thread = None

    def setUp(self):
        ''' Setup for the test case
        Initialises the temp database with some data
        '''
        self.user_1 = UserFactory.create(username="username_1",password="password")
        self.thread = ThreadsFactory.create(creating_user=self.user_1, title="title")

    def tearDown(self):
        ''' Cleanup any test data
        '''
        UserDetails.objects.all().delete()
        UserGalleries.objects.all().delete()
        UserStatuses.objects.all().delete()
        Threads.objects.all().delete()
        ThreadMessages.objects.all().delete()
        UserConnectionJunctions.objects.all().delete()
        UserThreadJunctions.objects.all().delete()
        User.objects.all().delete()

    def test_threadCreate(self):
        ''' Test
        Test if the endpoint handels
        Create
        '''
        # Logging the user in, and check logged in
        response = self.client.post(reverse('login'), {'username': 'username_1', 'password': 'password'})
        self.assertEqual(response.wsgi_request.user, self.user_1)

        # Setting up for the request
        csrf_token = self.client.cookies['csrftoken'].value
        headers = {'HTTP_X-CSRFToken': csrf_token}

        # Creating a thread: returns created status
        data = {
            'title': 'thread', 
            'csrfmiddlewaretoken': csrf_token
            }
        response = self.client.post(reverse('thread_api'), data, **headers)
        self.assertEqual(response.status_code, 201)

    @transaction.atomic
    def test_threadDelete(self):
        ''' Test
        Test if the endpoint handels
        Delete & Delete Non Existing
        '''
        # Logging the user in, and check logged in
        response = self.client.post(reverse('login'), {'username': 'username_1', 'password': 'password'})
        self.assertEqual(response.wsgi_request.user, self.user_1)

        # Setting up for the request
        csrf_token = self.client.cookies['csrftoken'].value
        headers = {'HTTP_X-CSRFToken': csrf_token}

        # Deleting a thread: returns no content status
        response = self.client.delete(reverse('thread_api') + f'?thread_id={self.thread.id}', **headers)
        self.assertEqual(response.status_code, 204)

        # Deleting a thread that doesnt exist: returns not found status
        headers = {'HTTP_X-CSRFToken': csrf_token}
        response = self.client.delete(reverse('thread_api') + f'?thread_id=10001', **headers)
        self.assertEqual(response.status_code, 404)


class UserThreadJunctionTest(APITestCase):
    ''' Test for 'user_thread_junction_api' 
    '''
    user_1 = None
    user_2 = None
    thread = None
    user_thread_junction_1 = None

    def setUp(self):
        ''' Setup for the test case
        Initialises the temp database with some data
        '''
        self.user_1 = UserFactory.create(username="username_1",password="password")
        self.user_2 = UserFactory.create(username="username_2",password="password")
        self.thread = ThreadsFactory.create(creating_user=self.user_1, title="title")
        self.user_thread_junction_1 = UserThreadJunctionsFactory.create(user=self.user_1, thread=self.thread)

    def tearDown(self):
        ''' Cleanup any test data
        '''
        UserDetails.objects.all().delete()
        UserGalleries.objects.all().delete()
        UserStatuses.objects.all().delete()
        Threads.objects.all().delete()
        ThreadMessages.objects.all().delete()
        UserConnectionJunctions.objects.all().delete()
        UserThreadJunctions.objects.all().delete()
        User.objects.all().delete()

    @transaction.atomic
    def test_userThreadJunctionCreate(self):
        ''' Test
        Test if the endpoint handels
        Create & Create Duplicate
        '''
        # Logging the user in, and check logged in
        response = self.client.post(reverse('login'), {'username': 'username_1', 'password': 'password'})
        self.assertEqual(response.wsgi_request.user, self.user_1)

        # Setting up for the request
        csrf_token = self.client.cookies['csrftoken'].value
        headers = {'HTTP_X-CSRFToken': csrf_token}

        # Creating a user_thread_junction: returns created status
        data = {'user': self.user_2.id, 'thread': self.thread.id, 'csrfmiddlewaretoken': csrf_token}
        response = self.client.post(reverse('user_thread_junction_api'), data, **headers)
        self.assertEqual(response.status_code, 201)

        # Creating a duplicate user_thread_junction: returns client created error
        data = {'user': self.user_2.id, 'thread': self.thread.id, 'csrfmiddlewaretoken': csrf_token}
        response = self.client.post(reverse('user_thread_junction_api'), data, **headers)
        self.assertEqual(response.status_code, 400)

    @transaction.atomic
    def test_userThreadJunctionDelete(self):
        ''' Test
        Test if the endpoint handels
        Delete & Delete Non Existing
        '''
        # Logging the user in, and check logged in
        response = self.client.post(reverse('login'), {'username': 'username_1', 'password': 'password'})
        self.assertEqual(response.wsgi_request.user, self.user_1)

        # Setting up for the request
        csrf_token = self.client.cookies['csrftoken'].value
        headers = {'HTTP_X-CSRFToken': csrf_token}

        # Deleting a user_thread_junction: returns no content status
        response = self.client.delete(reverse('user_thread_junction_api') + f'?user_thread_junction_id={self.user_thread_junction_1.id}', **headers)
        self.assertEqual(response.status_code, 204)

        # Deleting a user_thread_junction that doesnt exist: returns not found status
        response = self.client.delete(reverse('user_thread_junction_api') + f'?user_thread_junction_id=10001', **headers)
        self.assertEqual(response.status_code, 404)

# I wrote this code -------------------------- End