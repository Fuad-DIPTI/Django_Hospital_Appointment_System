from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from .decorators import role_required
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request, 'home.html')

@role_required(['staff'])
def register_view(request):
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        login(request, user)

        return redirect('dashboard')

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.role == 'doctor':
                return redirect('dashboard')
            elif user.role == 'staff':
                return redirect('dashboard')
            else:
                return redirect('dashboard')

    return render(request, 'login.html')


@login_required()
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required()
def logout_view(request):
    logout(request)
    return redirect('login')