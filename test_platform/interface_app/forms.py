from django import forms
from interface_app.models import Testcase, Testtask


# class ModuleForm(forms.ModelForm):
#     class Meta:
#         model = Testcase
#         fields = ['module', 'name', 'req_url', 'req_method', 'req_header','req_ptype','req_parameter']
#         # exclude = ['create_time']


# class TesttaskForm(forms.ModelForm):
#     class Meta:
#         model = Testtask
#         fields = [ 'name', 'describe', 'cases', 'status']
#         # exclude = ['create_time']
