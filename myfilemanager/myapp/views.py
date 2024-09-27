from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from .middlewares import auth
from .models import Project
from .forms import ProjectForm
from django.contrib import messages
from .models import Profile
from .forms import UploadFileForm
from .models import UploadedFile
from django.conf import settings
import base64
import os
import requests


# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('login')
    else:
        initial_data = {'username':'','password1':'','password2':''}
        form = UserCreationForm(initial=initial_data)
    return render(request,'auth/register.html',{'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)

             # Check the user's role
            profile = Profile.objects.get(user=user)
            if profile.role == 'project_master':
                return redirect('dashboard')  # Redirect to project master dashboard
            elif profile.role == 'user':
                return redirect('user_dashboard')  # Redirect to user dashboard
            else:
                messages.error(request, "Unauthorized role.")
                return redirect('login')
    else:
        initial_data = {'username':'','password':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request,'auth/login.html',{'form': form})


@auth
def dashboard_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('dashboard')
    else:
        form = ProjectForm()

    # Fetch all projects regardless of the user's role
    projects = Project.objects.all()

    return render(request, 'dashboard.html', {'form': form, 'projects': projects})

def logout_view(request):
    logout(request)
    return redirect('login')



#project master












#upload 
from django.shortcuts import render
from .models import Project, UploadedFile
from .forms import UploadFileForm
from django.contrib import messages
from django.conf import settings
import os
import base64
import requests

def user_dashboard(request):
    # Get all projects the user is assigned to
    user_projects = Project.objects.filter(assigned_users=request.user)

    # Check if any of the user's projects have uploads enabled
    upload_enabled = user_projects.filter(upload_enabled=True).exists()

    if request.method == 'POST' and upload_enabled:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.files['file']
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(file_path, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            with open(file_path, 'rb') as f:
                file_content = f.read()
            encoded_file = base64.b64encode(file_content).decode('utf-8')

            payload = {
                "file_name": file.name,
                "file_content": encoded_file
            }

            response = requests.post('https://x2k3csuj2m.execute-api.ap-south-1.amazonaws.com/dev/upload', json={"body": payload})

            if response.status_code == 200:
                UploadedFile.objects.create(filename=file.name, user=request.user)
                messages.success(request, 'File uploaded successfully.')
            else:
                messages.error(request, 'File upload failed.')
    else:
        form = UploadFileForm()

    uploaded_files = UploadedFile.objects.filter(user=request.user)
    
    return render(request, 'user_dashboard.html', {
        'form': form,
        'uploaded_files': uploaded_files,
        'upload_enabled': upload_enabled,
        'user_projects': user_projects  # Pass the user's projects to the template
    })
