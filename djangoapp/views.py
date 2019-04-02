from django.shortcuts import render
from djangoapp.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    home = {'home_content' : 'Welcome'}
    return render(request, 'webthemes/index.html', context=home)

@login_required
def special(request):
    return HttResponse("You are logged in, Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == "POST":
        userform = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if userform.is_valid() and profile_form.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(userform.errors, profile_form.errors)
    else:
        userform = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'webthemes/register.html', {
                                        'user_form':userform,
                                        'profile_form':profile_form})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttResponse('Account not active')
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {} ".format(username, password))
            return HttResponse("invalid login details supplied!")
    else:
        return render(request, 'webthemes/login.html', {})
