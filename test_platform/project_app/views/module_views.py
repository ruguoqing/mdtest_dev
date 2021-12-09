from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from project_app.forms import ModuleForm
from project_app.models import Module,Project
from django.http import HttpResponse, HttpResponseRedirect



@login_required  # 判断用户是否登录
def module_manage(request):
    username = request.session.get('user', '')  # 读取浏览器session
    module_all = Module.objects.all()
    return render(request, 'module_manage.html', {
        'user': username,
        'modules': module_all,
        'type': 'list'
    })


@login_required
def add_module(request):
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():  # 进行数据校验
            data = form.cleaned_data  # 校验成功的值，会放在cleaned_data里。
            print(data)
            Module.objects.create(project=data['project'], name=data['name'], describe=data['describe'])
            module_all = Module.objects.all()
            return render(request, "module_manage.html", {'modules': module_all,
                                                          'type': 'list'})
    else:
        form = ModuleForm()
    return render(request, "module_manage.html", {"form": form, 'type': 'add'})


# @login_required
def edit_module(request, mid):
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():  # 进行数据校验
            # 校验成功
            model = Module.objects.get(id=mid)
            print(model)
            model.name = form.cleaned_data['name']
            model.describe = form.cleaned_data['describe']
            model.project = form.cleaned_data['project']
            model.save()
            # 校验成功的值，会放在cleaned_data里。
            return HttpResponseRedirect('/manage/module_manage/')

    else:
        if mid:
            form = ModuleForm(
                instance=Module.objects.get(id=mid)
            )
    return render(request, "module_manage.html", {"form": form, 'type': 'edit'})


def delete_module(request, mid):
    Module.objects.filter(id=mid).delete()
    return HttpResponseRedirect('/manage/module_manage/')