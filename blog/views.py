from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse


def login_view(request):
    if request.method == "GET":
        form = {
            'form': AuthenticationForm
        }
        return render(request, 'blog/adminLogin.html', form)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                try:
                    return HttpResponseRedirect(request.GET['next'])
                except KeyError:
                    return HttpResponseRedirect(reverse('blog-dashboard'))
            else:
                raise Http404
        else:
            raise Http404


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog-login'))


def home(request):
    return render(request, 'blog/home.html')


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


@login_required
def dashboard(request):
    return render(request, 'blog/userDashboard.html')


@login_required
def results(request):
    return render(request, 'blog/results.html')


@login_required
def upload_files(request):
    return render(request, 'blog/uploadFiles.html')


@login_required
def files(request):
    return render(request, 'blog/files.html')
