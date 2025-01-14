from django.shortcuts import redirect, render
from authuser.forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {username}')
            new_user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('core:index')
    else:
        
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'authuser/sign-up.html', context)
