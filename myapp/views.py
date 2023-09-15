from django.shortcuts import render
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from .forms import *
from .models import *
from .tasks import *

# I wrote this code -------------------------- Start
class RegisterView(CreateView):
    '''RegisterView
    An endpoint. Handling registering users, serving page and creating users

    Accepts: 'GET'
    'register/' -> Returns a html template page, inclusive of body forms
    
    Accepts: 'POST'
    'register/' -> Creates a user record
    data : {
        username: String
        email: String
        first_name: String
        last_name: String
        password1: String
        password2: String
    }
    returns 302 or error
    '''
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'myapp/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'register_form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../')
        return HttpResponse('User already exists', status=status.HTTP_400_BAD_REQUEST)

class LoginView(LoginView):
    '''LoginView
    An endpoint. Handling logging in users, serving page and logging in users

    Accepts: 'GET'
    'login/' -> Returns a html template page, inclusive of body forms
    
    login: 'POST'
    'login/' -> Logs in a user
    data : {
        username: String
        password: String
    }
    returns 302 or error
    '''
    form_class = LoginForm
    initial = {'key': 'value'}
    template_name = 'myapp/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'login_form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                request.session['user_id'] = user.id
                return HttpResponseRedirect('../')
            else:
                return HttpResponse('Account inactive', status=status.HTTP_403_FORBIDDEN)
        return HttpResponse('Invalid credentials', status=status.HTTP_400_BAD_REQUEST)

class UserUpdate(LoginRequiredMixin,UpdateView):
    '''UserUpdate
    An endpoint. Handling user updates, serving page and updates users

    Accepts: 'GET'
    'update_user/' -> Returns a html template page, inclusive of body forms
    
    login: 'POST'
    'update_user/' -> Updates a user reord
    data : {
        username: String
        email: String
        first_name: String
        last_name: String
        profile_image: File
        about_me: String
    }
    returns 200 or error
    '''
    model = User
    form_class = UpdateUserForm
    template_name = 'myapp/update_user.html'
    success_url = '/'

    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_user_form'] = UpdateUserForm(instance=self.request.user)
        context['update_user_details_form'] = UpdateUserDetailsForm(instance=self.request.user.UserDetails)
        context['user_status_form'] = UserStatusesForm()
        context['user_galleries_form'] = UserGalleriesForm()
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        user_details_form = UpdateUserDetailsForm(self.request.POST, self.request.FILES, instance=self.object.UserDetails)
        if user_details_form.is_valid():
            record = user_details_form.save()
            if 'profile_image' in self.request.FILES:
                make_profile_thumbnail.delay(record.pk)
        return super().form_valid(form)

class UserView(LoginRequiredMixin,View):
    '''UserView
    An endpoint. Handling user views, serving page for a user profile

    Accepts: 'GET'
    'user_view/?user_id=<pk>' -> Returns a html template page, inclusive of body forms
    '''
    model = User
    template_name = 'myapp/user_view.html'
    
    def get(self, request, *args, **kwargs):
        user_id = self.request.GET.get('user_id', None)
        if user_id:
            viewable_user = self.model.objects.get(id=user_id)
            return render(request, self.template_name, {'viewable_user': viewable_user})
        return HttpResponse('User doesnt exist', status=status.HTTP_404_NOT_FOUND)

class ThreadView(LoginRequiredMixin,View):
    '''ThreadView
    An endpoint. Handling thread views, serving page for a thread

    Accepts: 'GET'
    'thread/?thread_id=<pk>' -> Returns a html template page, inclusive of body forms
    '''
    model = Threads
    template_name = 'myapp/thread.html'
    
    def get(self, request, *args, **kwargs):
        thread_id_query = self.request.GET.get('thread_id', None)
        if thread_id_query:
            thread = self.model.objects.get(id=thread_id_query)
            return render(request, self.template_name, {'thread': thread, 'user_thread_junction_form': UserThreadJunctionForm(initial={'thread': thread_id_query})})
        return HttpResponse('Thread doesnt exist', status=status.HTTP_404_NOT_FOUND)
    
@login_required
def UserDashboard(request):
    '''UserDashboard
    An endpoint handeler. Returns the users dashbord, and forms
    '''
    return render(request, 'myapp/user_dashboard.html', {'thread_form': ThreadForm()})

@login_required
def Logout(request):
    '''Logout
    An endpoint handeler. Logs out a user and returns a 302
    '''
    logout(request)
    return HttpResponseRedirect('../')
# I wrote this code -------------------------- End