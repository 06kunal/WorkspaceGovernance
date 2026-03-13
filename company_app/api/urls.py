from django.urls import path

from company_app.api.views import WorkSpaceList, WorkSpaceDetail, ProjectList, ProjectDetail, TaskList, TaskDetail
urlpatterns = [
    
    path('workspaces/', WorkSpaceList.as_view(), name='workspace-list'),
    path('workspaces/<int:pk>/', WorkSpaceDetail.as_view(), name='workspace-detail'),
    
    path('workspaces/<int:pk>/project/', ProjectList.as_view(), name='project-list'),
    path('workspaces/<int:workspace_pk>/project/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    
    path('workspaces/<int:workspace_pk>/project/<int:project_pk>/tasks/', TaskList.as_view(), name='task-list'),
    path('workspaces/<int:workspace_pk>/project/<int:project_pk>/tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
]
