from django.shortcuts import redirect, render
from authuser.forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            name = form.cleaned_data.get('name')
            last_name = form.cleaned_data.get('last_name')
            messages.success(request, f'Account created for {name + " " + last_name}')
            new_user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('core:index')
    else:
        
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'authuser/sign-up.html', context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:index')
        else:
            messages.error(request, 'Email o contraseña incorrectos')
    return render(request, 'authuser/login.html')

def logout_view(request):
    logout(request)
    return redirect('core:index')
