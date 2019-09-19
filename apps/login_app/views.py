from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request,'login_app/index.html')

def registration(request):
    errors = User.objects.register_user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')

    if request.method == 'POST':
        # encode the password
        pw_hash = bcrypt.hashpw(request.POST['new_password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['reg_email'], password = pw_hash)

    return redirect('/')

def auth_user(request):
    login_errors = User.objects.login_user_validator(request.POST) 
    if len(login_errors) > 0:
        for key, value in login_errors.items():
            messages.error(request, value)
        return redirect ('/')
    if request.method == 'POST':
        user = User.objects.filter(email = request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['user_password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/success')
            else: 
                print('Incorrect password, try again')
                return redirect('/')
    return redirect('/')

def user_logged(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['user_id'])
        context = {
            'user_info' : user
        }
        return render(request, 'login_app/landing.html', context)

def clear_session(request):
    del request.session['user_id']
    return redirect('/')