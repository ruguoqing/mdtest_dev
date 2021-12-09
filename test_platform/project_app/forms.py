from django import forms
from project_app.models import Project, Module


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'describe', 'status']


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['project', 'name', 'describe']
        # exclude = ['create_time']

