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
    create_time = models.DateTimeField('创建时间', auto_now=True)

    def __str__(self):
        return self.name
