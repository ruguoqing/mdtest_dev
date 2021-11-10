
import requests
import json
from test_platform import common
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from interface_app.models import Testcase, Testtask
from project_app.models import Module, Project
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here

# 用例列表
def task_manage(request):
    tasks = Testtask.objects.all()
    paginator = Paginator(tasks, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果不是整型，取第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果超出范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'task_manage.html', {'type': 'list',
                                                'tasks': contacts
                                                })


def add_task(request):
    if request.method == 'GET':
        return render(request, 'add_task.html', {'type': 'add',
                                                   })
    else:
        return HttpResponse('404')




# 选择一个用例点击调试
def debug_case(request, cid):
    if request.method == 'GET':
        testcase = Testcase.objects.get(id=cid)
        module_obj = Module.objects.get(name=testcase.module)
        return render(request, 'debug_case.html', {'type': 'debug_case',
                                                   'cid': cid,
                                                   'project': module_obj.project,
                                                   'module': testcase.module,
                                                   'name': testcase.name,
                                                   'url': testcase.req_url,
                                                   'method': testcase.req_method,
                                                   'header': testcase.req_header,
                                                   'ptype': testcase.req_ptype,
                                                   'parameter': testcase.req_parameter,
                                                   })


# 删除用例
def delete_case(request, cid):
    if request.method == 'GET':
        Testcase.objects.get(id=cid).delete()
    return HttpResponseRedirect('/interface/case_manage/')



# 获取用例
def get_case_info(request):
    datalist = []
    project_list = Project.objects.all()
    for project in project_list:
        module_list = Module.objects.filter(project_id=project.id)
        for module in module_list:
            case_list = Testcase.objects.filter(module_id=module.id)
            for case in case_list:
                case_info = {'case_id': case.id, 'case': project.name + '-->' + module.name + '-->' + case.name}
                datalist.append(case_info)
    if len(datalist) != 0:
        return JsonResponse({'success': 'true', 'data': datalist})



def save_case(request):
    if request.method == 'POST':
        module = request.POST.get('module')
        name = request.POST.get('name')
        url = request.POST.get('req_url')
        method = request.POST.get('req_method')
        header = request.POST.get('req_header')
        ptype = request.POST.get('req_ptype')
        parameter = request.POST.get('parameter')
        # payload = json.loads(parameter.replace("'", "\""))

        if module == '' or method == '' or url == '':
            return HttpResponse('必选参数不能为空')

        module_obj = Module.objects.get(name=module)
        case = Testcase.objects.create(module=module_obj, name=name, req_url=url, req_method=method,
                                       req_header=header, req_ptype=ptype, req_parameter=parameter)
        if case is not None:
            return HttpResponse('保存成功')
    else:
        return HttpResponse('保存失败')


def update_case(request, cid):
    if request.method == 'POST':
        module = request.POST.get('module')
        name = request.POST.get('name')
        url = request.POST.get('req_url')
        method = request.POST.get('req_method')
        header = request.POST.get('req_header')
        ptype = request.POST.get('req_ptype')
        parameter = request.POST.get('parameter')

        if module == '' or method == '' or url == '':
            return HttpResponse('必选参数不能为空')

        module_obj = Module.objects.get(name=module)
        Testcase.objects.select_for_update().filter(id=cid).update(module=module_obj, name=name, req_url=url,
                                                                          req_method=method,
                                                                          req_header=header, req_ptype=ptype,
                                                                          req_parameter=parameter)
        return HttpResponse('保存成功')

    else:
        return HttpResponse('保存失败')


