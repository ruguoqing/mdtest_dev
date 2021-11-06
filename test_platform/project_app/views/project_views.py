from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from project_app.forms import ProjectForm
from project_app.models import Project
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.


@login_required  # 判断用户是否登录
def project_manage(request):
    username = request.session.get('user', '')  # 读取浏览器session
    project_all = Project.objects.all()
    # username = request.COOKIES.get('user', '')  # 读取浏览器cookie
    return render(request, 'project_manage.html', {
        'user': username,
        'projects': project_all,
        'type': 'list'
    })


# @login_required  # 判断用户是否登录
# def add_project(request):
#     return render(request, 'project_manage.html', {
#         'type': 'add'
#     })

@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():  # 进行数据校验
            # 校验成功
            data = form.cleaned_data  # 校验成功的值，会放在cleaned_data里。
            print(data)
            Project.objects.create(name=data['name'], describe=data['describe'], status=data['status'])
            project_all = Project.objects.all()
            return render(request, "project_manage.html", {'projects': project_all,
                                                           'type': 'list'})
    else:
        form = ProjectForm
    return render(request, "project_manage.html", {"form": form, 'type': 'add'})


# @login_required
def edit_project(request, pid):
    # project = Project.objects.filter(id=pid)
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():  # 进行数据校验
            # 校验成功
            model = Project.objects.get(id=pid)
            print(model)
            model.name = form.cleaned_data['name']
            model.describe = form.cleaned_data['describe']
            model.status = form.cleaned_data['status']
            model.save()
            # 校验成功的值，会放在cleaned_data里。
            return HttpResponseRedirect('/manage/project_manage/')

    else:
        if pid:
            form = ProjectForm(
                instance=Project.objects.get(id=pid)
            )
    return render(request, "project_manage.html", {"form": form, 'type': 'edit'})


def delete_project(request, pid):
    Project.objects.filter(id=pid).delete()
    return HttpResponseRedirect('/manage/project_manage/')