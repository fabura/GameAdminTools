from django.contrib.auth.decorators import login_required
from web.users.models import UserProfile, UserProfileForm

__author__ = 'Bulat'
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf

def user_login(request, next='/index'):
    c = {}
    c.update(csrf(request))
    if 'next' in request.GET:
        next = request.GET['next']
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(to=next)
        else:
            c["error_message"] = "Authentification error. Try again"
            return render_to_response('users/login.html', c)
    else:
        return render_to_response('users/login.html', c)


def register(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        username_ = request.POST['username']
        password_ = request.POST['password']
        if User.objects.filter(username__iexact=username_).count() == 0:
            user = User.objects.create_user(username=username_, password=password_)
            user.save()
            user = authenticate(username=username_, password=password_)
            if user is not None:
                print("You provided a correct username and password!")
            return redirect("/index")
        else:
            c["error_message"] = "This username already in use"
            return render_to_response('users/register.html', c)
    else:
        return render_to_response('users/register.html', c)

@login_required(login_url='login')
def user_info(request):
    c = {}
    c.update(csrf(request))
    try:
        user_id = request.user.id
        profile = UserProfile.objects.get(user__id=user_id)
    except:
        raise UserWarning()
    if not profile:
        raise UserWarning()

    form = None
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            user_profile = form.save()
            user_profile.save()
    elif request.method == "GET":
        form = UserProfileForm(instance=profile)
    c['form'] = form
    return render_to_response('users/info.html', c)

