import os
import json
from test_platform import common
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from interface_app.models import Testcase, Testtask, Taskresult
from project_app.models import Module, Project
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from interface_app.apps import TASK_DIR, RUN_TASK_FILE
from interface_app.extend.thread_task import ThreadTask


# Create your views here

# 任务列表
def task_manage(request):
    testtasks = Testtask.objects.all().order_by('id')
    paginator = Paginator(testtasks, 10)
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


# 添加任务
def add_task(request):
    if request.method == 'GET':
        return render(request, 'add_task.html', {'type': 'add',
                                                 'page': 'add',
                                                 })
    else:
        return HttpResponse('404')


# 选择一个任务编辑
def edit_task(request, tid):
    if request.method == 'GET':
        testtask_obj = Testtask.objects.get(id=tid)
        return render(request, 'add_task.html', {'type': 'add',
                                                 'page': 'edit',
                                                 'name': testtask_obj.name,
                                                 'describe': testtask_obj.describe,
                                                 'cases': testtask_obj.cases
                                                 })


# 删除用例
def delete_task(request, tid):
    if request.method == 'GET':
        Testtask.objects.get(id=tid).delete()
    return HttpResponseRedirect('/interface/task_manage/')


# 获取用例
def get_case_info(request):
    if request.method == 'GET':
        # tid = request.GET.get()
        # print('地址',tid)
        # task_object = Testtask.objects.get(id=tid)
        # cid_list = task_object.cases
        # print(cid_list)
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


# 获取用例
def get_selected_cases(request):
    if request.method == 'POST':
        tid = request.POST.get('tid')
        print('传过来的id', tid)
        task_object = Testtask.objects.get(id=tid)
        cid_list = task_object.cases
        print(cid_list)
        return JsonResponse({'success': 'true', 'data': cid_list})


def save_task(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        describe = request.POST.get('describe')
        cases = request.POST.get('cases')

        if name == '':
            return common.response_failed('任务名称不能为空')

        task = Testtask.objects.create(name=name, describe=describe, cases=cases)
        if task is not None:
            return common.response_succeed('保存成功')
    else:
        return common.response_failed('保存失败')


def run_task(request, tid):
    if request.method == 'GET':
        ThreadTask(tid).run()
        return HttpResponseRedirect('/interface/task_manage/')
    else:
        return common.response_failed('运行失败')


def task_result(request, tid):
    if request.method == 'GET':
        results = Taskresult.objects.filter(task=tid)
        return render(request, 'result_list.html', {'type': 'list',
                                                    'results': results,
                                                    })

