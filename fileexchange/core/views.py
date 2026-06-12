from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import File
from django.contrib.auth import logout
import os

ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png'],
    'video': ['.mp4', '.avi'],
    'audio': ['.mp3', '.wav'],
    'text': ['.txt', '.pdf'],
    '3d': ['.obj', '.fbx']
}

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def upload_file(request, file_type):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()

            if ext not in ALLOWED_EXTENSIONS.get(file_type, []):
                return render(request, 'core/upload.html', {
                    'file_type': file_type,
                    'error': 'Nepodporovaný typ souboru'
                })

            print("UPLOAD:", uploaded_file.name)

            new_file = File.objects.create(
                user=request.user,
                file=uploaded_file,
                original_name=uploaded_file.name,
                file_type=file_type
            )

            print("SAVED:", new_file.file.name)


        return redirect('file_list', file_type=file_type)

    return render(request, 'core/upload.html', {
        'file_type': file_type
    })


@login_required
def file_list(request, file_type):
    files = File.objects.filter(user=request.user, file_type=file_type)

    return render(request, 'core/file_list.html', {
        'files': files,
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
def delete_file(request, file_id):
    file = File.objects.get(id=file_id, user=request.user)
    file.file.delete()
    file.delete()
    return redirect('file_list', file_type=file.file_type)



@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
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

@login_required
def share_file(request, file_id):

    file = File.objects.get(id=file_id)

    if file.user != request.user:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')

        try:
            target_user = User.objects.get(username=username)
            if target_user == request.user:
                return render(
                    request,
                    'core/share_file.html',
                    {
                        'file': file,
                        'error': 'Cannot share file with yourself'
                    }
                )
            if target_user in file.shared_with.all():
                return render(
                    request,
                    'core/share_file.html',
                    {
                        'file': file,
                        'error': 'Already shared with this user'
                    }
                )

            file.shared_with.add(target_user)

            return redirect('file_list', file_type=file.file_type)

        except User.DoesNotExist:

            return render(
                request,
                'core/share_file.html',
                {
                    'file': file,
                    'error': 'User not found'
                }
            )

    return render(
        request,
        'core/share_file.html',
        {
            'file': file
        }
    )

@login_required
def shared_files(request):

    files = File.objects.filter(
        shared_with=request.user
    )

    return render(
        request,
        'core/shared_files.html',
        {
            'files': files
        }
    )


@login_required
def unshare_file(request, file_id, user_id):

    file = File.objects.get(id=file_id)

    if file.user != request.user:
        return redirect('dashboard')

    user = User.objects.get(id=user_id)

    file.shared_with.remove(user)

    return redirect(
        'file_list',
        file_type=file.file_type
    )