from django.db import models
from project_app.models import Module

# Create your models here.


class Testcase(models.Model):
    """
    测试用例表
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField('名称', max_length=100, default='')
    req_url = models.TextField('地址', default='')
    req_method = models.CharField('方法', max_length=100, default='')
    req_header = models.TextField('请求头', default='')
    req_ptype = models.CharField('参数类型', max_length=100)
    req_parameter = models.TextField('参数', default='')
    res_assert = models.TextField('验证', default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name


class Testtask(models.Model):
    """
    任务管理表
    """
    name = models.CharField('名称', max_length=100, default='')
    describe = models.TextField('描述', default='')
    cases = models.TextField('关联用例', default='')
    status = models.IntegerField('状态', default=0)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name


class Taskresult(models.Model):
    """
    任务管理表
    """
    task = models.ForeignKey(Testtask, on_delete=models.CASCADE)
    name = models.CharField('名称', max_length=100, default='')
    tests = models.IntegerField('运行数', default='')
    failures = models.IntegerField('失败数', default='')
    skipped = models.IntegerField('跳过数', default='')
    errors = models.IntegerField('错误数', default='')
    time = models.FloatField('运行时长', default='')
    result = models.TextField('结果描述', default='')
    run_time = models.DateTimeField('执行时间')

    def __str__(self):
        return self.name