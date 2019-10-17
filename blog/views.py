from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def home(request):
    return render(request, 'blog/home.html')


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def login(request):
    form = {
        'form': UserCreationForm
    }
    return render(request, 'blog/adminLogin.html', form)


def dashboard(request):
    return render(request, 'blog/userDashboard.html')


def results(request):
    return render(request, 'blog/results.html')

def uploadFiles(request):
    return render(request, 'blog/uploadFiles.html')