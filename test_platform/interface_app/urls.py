from django.urls import path
from interface_app.views import case_views
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
    path('get_project_list', case_views.get_project_list),
    path('search_case/', case_views.search_case)

]

