from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import File

@login_required
def upload_file(request, file_type):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            File.objects.create(
                user=request.user,
                file=uploaded_file,
                file_type=file_type
            )

        return redirect('dashboard')

    return render(request, 'core/upload.html', {
        'file_type': file_type
    })

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # jednoduchá kontrola (zatím basic)
        if User.objects.filter(username=username).exists():
            return render(request, 'core/register.html', {
                'error': 'Uživatel už existuje'
            })

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'core/register.html')


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # zatím neexistuje
        else:
            return render(request, 'core/login.html', {
                'error': 'Špatné přihlašovací údaje'
            })

    return render(request, 'core/login.html')