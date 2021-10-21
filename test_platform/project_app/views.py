from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from project_app.models import Project

# Create your views here.


@login_required  # 判断用户是否登录
def project_manage(request):
    username = request.session.get('user', '')  # 读取浏览器session
    project_all = Project.objects.all()
    # username = request.COOKIES.get('user', '')  # 读取浏览器cookie
    return render(request, 'project_manage.html', {
        'user': username,
        'projects': project_all
        })
