from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm,ProjectForm
from .models import UserProfile,Project
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

def home(request):
    registered_users = UserProfile.objects.all()
    return render(request, 'home.html', {'registered_users': registered_users})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def upload_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('home')
    else:
        project_form = ProjectForm()
    return render(request, 'upload_project.html', {'project_form': project_form})

def view_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    projects = Project.objects.filter(user=user)
    return render(request, 'user_profile.html', {'user': user, 'projects': projects})
