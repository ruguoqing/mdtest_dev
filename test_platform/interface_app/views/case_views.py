import requests
import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from interface_app.models import Testcase
from project_app.models import Module, Project
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here

# 用例列表
def case_manage(request):
    testcases = Testcase.objects.all()
    paginator = Paginator(testcases, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果不是整型，取第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果超出范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'case_manage.html', {'type': 'list',
                                                'testcases': contacts
                                                })


# 搜索用例名称
def search_case(request):
    if request.method == 'GET':
        case_name = request.GET.get('case_name', '')
        print(case_name)
        testcases = Testcase.objects.filter(name__contains=case_name)
        paginator = Paginator(testcases, 10)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果不是整型，取第一页
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果超出范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'case_manage.html', {'type': 'list',
                                                    'testcases': contacts
                                                    })

    else:
        return HttpResponse('404')


# 创建用例
def add_debug(request):
    if request.method == 'GET':
        return render(request, 'api_debug.html', {'type': 'debug',
                                                  })
    else:
        return HttpResponse('404')


# 选择一个用例点击调试
def debug_case(request, cid):
    if request.method == 'GET':
        testcase = Testcase.objects.get(id=cid)
        print(testcase.module)
        module_obj = Module.objects.get(name=testcase.module)
        print(module_obj.project)
        return render(request, 'debug_case.html', {'type': 'debug_case',
                                                   'project': module_obj.project,                                                   'module': testcase.module,
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


# 调试用例
def api_debug(request):
    if request.method == 'POST':
        url = request.POST.get('req_url')
        method = request.POST.get('req_method')
        header = request.POST.get('req_header')
        header = json.loads(header.replace("'", "\""))
        ptype = request.POST.get('req_ptype')
        parameter = request.POST.get('parameter')
        payload = json.loads(parameter.replace("'", "\""))

        if method == 'get':
            r = requests.get(url, data=payload)
        if method == 'post':
            r = requests.post(url, headers=header, data=payload)
        print(r.text)
        return HttpResponse(r.text)
    else:
        return render(request, 'api_debug.html', {'type': 'debug',
                                                  })


# 获取项目和模块列表
def get_project_list(request):
    datalist = []
    project_list = Project.objects.all()
    for project in project_list:
        module_list = Module.objects.filter(project=project.id)
        if len(module_list) != 0:
            module_name = []
            for module in module_list:
                module_name.append(module.name)
            datalist.append({'name': project.name, 'moduleList': module_name})

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

# https://www.cnblogs.com/mzc1997/p/7813801.html
# requests.get('http://httpbin.org/get')
# requests.post('http://httpbin.org/post'),{"name":"tom","age":"22"}
# requests.put('http://httpbin.org/put')
# requests.delete('http://httpbin.org/delete')
# requests.head('http://httpbin.org/get')
# requests.options('http://httpbin.org/get')
