from django.http import JsonResponse


# 接口返回成功
def response_successed(message='请求成功', data={}):
    content = {
        'success': 'True',
        'msg': message,
        'data': data
    }
    return JsonResponse(content)


# 接口返回失败
def response_failed(message='参数错误', data={}):
    content = {
        'success': 'False',
        'msg': message,
        'data': data
    }
    return JsonResponse(content)
