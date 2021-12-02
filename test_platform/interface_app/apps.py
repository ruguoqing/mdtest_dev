from django.apps import AppConfig
from test_platform.settings import BASE_DIR
import os


class InterfaceAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'interface_app'


# 配置任务用例路径
TASK_DIR = os.path.join(BASE_DIR, 'resourse/tasks/')

# 配置运行任务路径
RUN_TASK_FILE = os.path.join(BASE_DIR, 'interface_app/extend/task_run.py')
