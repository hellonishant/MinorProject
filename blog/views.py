import base64
import io
import os

import PIL.Image as Image
import matplotlib.pyplot as plt
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify

from Blog import settings
from .models import File as FileModel, Result


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

        r = [
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
                # department_id=data.loc[idx, 'Department_ID'],
                department_name=branch,
                section=data.loc[idx, 'section']
            )
            for idx in data.index
        ]
        Result.objects.bulk_create(r)
        return HttpResponseRedirect(reverse('files'))


@login_required
def files(request):
    context = {'files': FileModel.objects.all()}
    return render(request, 'blog/files.html', context)


@login_required
def download(request, pk):
    f = FileModel.objects.all().get(id=pk)
    file_path = settings.BASE_DIR + f.url
    fh = open(file_path, 'rb')
    response = HttpResponse(fh.read(), content_type="application/csv")
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
    return response


@login_required
def delete(request, pk):
    f = FileModel.objects.all().get(id=pk)
    file_path = settings.BASE_DIR + f.url
    r = Result.objects.all().filter(semester_name=f.sem, department_name=f.branch)
    f.delete()
    r.delete()
    os.remove(file_path)
    return HttpResponseRedirect(reverse('files'))


@login_required
def result_search(request):
    if request.method == "GET":
        return render(request, 'blog/searchRollNo.html')
    else:
        return HttpResponseRedirect(reverse('student-result', args=(request.POST['rollNo'],)))


@login_required
def result(request, roll_no):
    r = Result.objects.all().filter(student_id=roll_no)

    avg = 0
    i = 0
    predict = 0
    marks = []
    s = []

    for r1 in r:
        i = i + 1
        avg = avg + r1.percentage
        s.insert(len(s), "Sem " + r1.semester_name)
        marks.insert(len(marks), r1.percentage)

    if i != 0:
        predict = round(avg/i, 2)

    fig = plt.figure(figsize=(9, 3))
    plt.subplot(131)
    plt.bar(s, marks)
    plt.subplot(132)
    plt.scatter(s, marks)
    plt.subplot(133)
    plt.plot(s, marks)
    plt.suptitle('Result')
    canvas = fig.canvas
    buf, size = canvas.print_to_buffer()
    image = Image.frombuffer('RGBA', size, buf, 'raw', 'RGBA', 0, 1)
    buffer = io.BytesIO()
    image.save(buffer, 'PNG')
    graphic = buffer.getvalue()
    graphic = base64.b64encode(graphic)
    buffer.close()

    if len(r) > 7:
        context = {
            'results': r,
            'predict': False,
            'graph': str(graphic)[2:-1],
        }
    else:
        context = {
            'results': r,
            'predict': True,
            'count': len(s),
            'p1': predict - 2,
            'p2': predict + 2,
            'graph': str(graphic)[2:-1],
        }

    return render(request, 'blog/rollNoResults.html', context)


@login_required
def results(request, dep, sem, section):
    if section == 'All':
        context = {'results': Result.objects.all().filter(department_name=dep, semester_name=sem)}
    else:
        context = {'results': Result.objects.all().filter(department_name=dep, semester_name=sem, section=section)}

    return render(request, 'blog/results.html', context)


def home(request):
    return render(request, 'blog/home.html')


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


@login_required
def dashboard(request):
    return render(request, 'blog/userDashboard.html')
