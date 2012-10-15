__author__ = 'Bulat'
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf

def user_login(request, next='/index'):
    c = {}
    c.update(csrf(request))
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
            user = authenticate(username='john', password='secret')
            if user is not None:
                print("You provided a correct username and password!")
            return redirect("/series")
        else:
            c["error_message"] = "This username already in use"
            return render_to_response('users/register.html', c)
    else:
        return render_to_response('users/register.html', c)
