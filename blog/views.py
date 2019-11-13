import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import smart_str
from django.utils.text import slugify
from .models import File as FileModel, Result
import pandas as pd


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


@login_required
def upload_files(request):
    if request.method == "GET":
        return render(request, 'blog/uploadFiles.html')
    else:
        file = request.FILES['fileUpload']
        sem = request.POST['semesterSelector']
        branch = request.POST['branchSelector']
        description = request.POST['fileDescription']

        fs = FileSystemStorage()
        filename = fs.save(slugify(branch) + '_' + slugify(sem) + '_' + file.name, file)
        uploaded_file_url = fs.url(filename)

        FileModel.objects.create(
            sem=sem,
            branch=branch,
            description=description,
            file_name=file.name,
            url=uploaded_file_url
        )

        data = pd.read_csv('media/' + slugify(branch) + '_' + slugify(sem) + '_' + file.name)
        data = data.fillna(0)

        result = [
            Result(
                student_id=data.loc[idx, 'Student_ID'],
                semester_name=sem,
                paper_1=data.loc[idx, 'Paper 1'],
                paper_2=data.loc[idx, 'Paper 2'],
                paper_3=data.loc[idx, 'Paper 3'],
                paper_4=data.loc[idx, 'Paper 4'],
                paper_5=data.loc[idx, 'Paper 5'],
                paper_6=data.loc[idx, 'Paper 6'],
                paper_7=data.loc[idx, 'Paper 7'],
                percentage=data.loc[idx, 'percentage'],
                total_marks=data.loc[idx, 'sum'],
                department_id=data.loc[idx, 'Department_ID'],
                department_name=branch,
                section=data.loc[idx, 'Section']
            )
            for idx in data.index
        ]

        Result.objects.bulk_create(result)

        return HttpResponseRedirect(reverse('files'))


@login_required
def files(request):
    context = {'files': FileModel.objects.all()}
    return render(request, 'blog/files.html', context)


@login_required
def download(request, pk):
    f = FileModel.objects.all().get(id=pk)
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(f.file_name)
    response['X-Sendfile'] = smart_str(f.url)
    return response


@login_required
def delete(request, pk):
    f = FileModel.objects.all().get(id=pk)
    f.delete()
    return HttpResponseRedirect(reverse('files'))


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
