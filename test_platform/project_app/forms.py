from django import forms
from django.forms import ModelForm
from project_app.models import Project


# class ProjectForm(forms.Form):
#     name = forms.CharField(label='名称', max_length=100)
#     describe = forms.CharField(label='描述', widget=forms.Textarea)
#     status = forms.BooleanField(label='状态')


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'describe', 'status']
