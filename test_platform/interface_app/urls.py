from django.urls import path
from interface_app.views import case_views, task_views
from user_app import views

urlpatterns = [
    # 用例管理
    path('case_manage/', case_views.case_manage),
    path('case_manage/logout/', views.logout),
    path('add_debug/', case_views.add_debug),
    path('debug_case/<int:cid>/', case_views.debug_case),
    path('delete_case/<int:cid>/', case_views.delete_case),
    path('api_debug/', case_views.api_debug),
    path('save_case/', case_views.save_case),
    path('update_case/<int:cid>/', case_views.update_case),
    path('get_project_list', case_views.get_project_list),
    path('search_case/', case_views.search_case),
    path('api_assert/', case_views.api_assert),

    #任务管理
    path('task_manage/', task_views.task_manage),
    path('task_manage/logout/', views.logout),
    path('add_task/', task_views.add_task),
    path('get_case_info', task_views.get_case_info),
    path('get_selected_cases', task_views.get_selected_cases),
    path('save_task/', task_views.save_task),
    path('edit_task/<int:tid>/', task_views.edit_task),
    path('delete_task/<int:tid>/', task_views.delete_task),
    path('run_task/<int:tid>/', task_views.run_task),
    path('task_result/<int:tid>/', task_views.task_result),

]

