
import requests
import json
from test_platform import common
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from interface_app.models import Testcase
from project_app.models import Module, Project
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here

# 用例列表
def case_manage(request):
    testcases = Testcase.objects.all().order_by('id')
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
        paginator = Paginator(testcases, 5)
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


# 创建用例，
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


# 调试用例
def api_debug(request):
    if request.method == 'POST':
        url = request.POST.get('req_url')
        method = request.POST.get('req_method')
        header = request.POST.get('req_header')
        ptype = request.POST.get('req_ptype')
        parameter = request.POST.get('parameter')
        # print('请求头' + header, '参数' + parameter)
        try:
            header = json.loads(header.replace("'", "\""))
            if type(header) == int:
                return common.response_failed('请求头输入错误')
        except json.JSONDecodeError:
            return common.response_failed('请求头输入错误')
        try:
            parameter = json.loads(parameter.replace("'", "\""))
            if type(parameter) == int:
                return common.response_failed('参数输入错误')
        except json.JSONDecodeError:
            return common.response_failed('参数输入错误')
        if method == 'get':
            r = requests.get(url, headers=header, data=parameter)
        if method == 'post':
            r = requests.post(url, headers=header, data=parameter)
        return common.response_succeed(data=r.text)


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


def api_assert(request):
    if request.method == 'POST':
        assert_text = request.POST.get('assert_text')
        assert_list = assert_text.split()
        result_text = request.POST.get('result_text')
        assert_error = []
        if assert_text == '' or result_text == '':
            return common.response_failed('断言或者接口返回不能为空')

        for ast in assert_list:
            try:
                assert ast in result_text
            except AssertionError:
                assert_error.append(ast)
        if len(assert_error) > 0:
            return common.response_failed('验证失败，请检查以下断言: ', assert_error)
        else:
            return common.response_succeed('验证成功')



# https://www.cnblogs.com/mzc1997/p/7813801.html
# requests.get('http://httpbin.org/get')
# requests.post('http://httpbin.org/post'),{"name":"tom","age":"22"}
# requests.put('http://httpbin.org/put')
# requests.delete('http://httpbin.org/delete')
# requests.head('http://httpbin.org/get')
# requests.options('http://httpbin.org/get')
