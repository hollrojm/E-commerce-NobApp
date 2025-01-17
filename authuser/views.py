from django.shortcuts import redirect, render
from authuser.forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from authuser.models import User


#User = settings.AUTH_USER_MODEL

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
    if request.user.is_authenticated:
       messages.info(request, 'Ya has iniciado sesión')
       return redirect('core:index')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(email=email, password=password)
       
            if user is not None:
                login(request, user)
                messages.success(request, f' Bienvenido {user.name}!')
                return redirect('core:index')
            else:
                messages.warning(request, f'Usuario o contraseña incorrectos')

        except:
            messages.error(request, f'Usuario {email} no encontrado')
        
        
    
    
    return render(request, 'authuser/sign-in.html')


         

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión')
    return redirect('sign-in')
