from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

# I wrote this code -------------------------- Start
class RegisterForm(UserCreationForm):
    '''RegisterForm
    A form. Handling the creation of users
    '''
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control',}))
    email = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control',}))
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'First Name',
        'class': 'form-control',}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Last Name',
        'class': 'form-control',}))
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',}))
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    '''LoginForm
    A form. Handling loggin in of users
    '''
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control',}))
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
        'name': 'password',}))

    class Meta:
        model = User
        fields = ['username', 'password']

class UpdateUserDetailsForm(forms.ModelForm):
    '''UpdateUserDetailsForm
    A form. Handling user_details updates
    '''
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    about_me = forms.CharField(required=False, max_length=500, widget=forms.Textarea(attrs={
        'placeholder': 'About me',
        'class': 'form-control', 
        'rows': 2}))
    
    class Meta:
        model = UserDetails
        fields = ['profile_image', 'about_me']

class UpdateUserForm(forms.ModelForm):
    '''UpdateUserForm
    A form. Handling user updates
    '''
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control',}))
    email = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control',}))
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'First Name',
        'class': 'form-control',}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Last Name',
        'class': 'form-control',}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserConnectionJunctionsForm(forms.ModelForm):
    '''UserConnectionJunctionsForm
    A form. Handling user_connection_junction creations
    '''
    class Meta:
        model = UserConnectionJunctions
        fields = ['user','user_connection']

class ThreadForm(forms.ModelForm):
    '''ThreadForm
    A form. Handling thread creations
    '''
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Title',
        'class': 'form-control',}))
    
    class Meta:
        model = Threads
        fields = ['title']

class UserStatusesForm(forms.ModelForm):
    '''UserStatusesForm
    A form. Handling user_status creations
    '''
    status = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Status',
        'class': 'form-control',}))
    
    class Meta:
        model = UserStatuses
        fields = ['status']

class UserGalleriesForm(forms.ModelForm):
    '''UserGalleriesForm
    A form. Handling user_galleries creations
    '''
    gallery_image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    
    class Meta:
        model = UserGalleries
        fields = ['gallery_image']

class UserThreadJunctionForm(forms.ModelForm):
    '''UserThreadJunctionForm
    A form. Handling user_thread_junction creations
    '''
    user = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'placeholder': 'UserID',
        'class': 'form-control',}))
    thread = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'placeholder': 'ThreadID',
        'readonly':'True',
        'class': 'form-control',}))
    
    class Meta:
        model = UserThreadJunctions
        fields = ['user', 'thread']
# I wrote this code -------------------------- End