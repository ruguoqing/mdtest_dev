from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
#主要代码逻辑


def index(request):
    return render(request, 'index.html')

# def index(request):
#     return HttpResponse(content='''
#     <form action="form_action.asp" method="get">
#         账户: <input type="text" name="username" />
#         密码: <input type="text" name="password" />
#         <input type="submit" value="Submit" />
#     </form>
#          ''')

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == '' or password == '':
            return render(request, 'index.html', {'error': '账户或者密码为空'})
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                return render(request, 'project_manage.html', {'error': 'success'})
            else:
                return render(request, 'index.html', {'error': '用户名或密码错误'})

        # if username == 'admin' and password == '123456':
        #     return render(request, 'project_manage.html', {'error': 'success'})
        # else:
        #     return render(request, 'index.html', {'error': '用户名或密码错误'})
