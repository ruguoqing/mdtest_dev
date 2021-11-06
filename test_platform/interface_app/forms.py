from django import forms
from interface_app.models import Testcase


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Testcase
        fields = ['module', 'name', 'req_url', 'req_method', 'req_header','req_ptype','req_parameter','create_time']
        # exclude = ['create_time']
