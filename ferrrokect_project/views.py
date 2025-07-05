# ferrrokect_project/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages # Para mostrar mensajes al usuario

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ahora puedes iniciar sesión.')
            return redirect('login') # Redirige a la página de login
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})