from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('lead_list')  # Redirect to lead list after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'register.html', {'error': "Passwords do not match."})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': "Username already exists."})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': "Email already exists."})
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        user = authenticate(username=username, password=password1)
        login(request, user)
        return redirect('lead_list')  # Redirect to lead list after registration
    else:
        return render(request, 'register.html')