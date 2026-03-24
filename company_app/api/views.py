from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from company_app.models import WorkSpace, WorkSpaceUser, Project, Task, ProjectUser
from company_app.api.serializers import WorkSpaceSerializer, WorkSpaceUserSerializer, ProjectSerializer, TaskSerializer, ProjectUserSerializer
from company_app.api.permissions import WorkSpaceUserPermission, WorkSpaceUserDetailPermission, ProjectUserPermission, ProjectUserDetailPermission, WorkSpacePermission, WorkSpaceDetailPermission, ProjectListPermission, ProjectDetailPermission




class WorkSpaceUserList(generics.ListCreateAPIView):
    
    serializer_class = WorkSpaceUserSerializer
    permission_classes = [WorkSpaceUserPermission] 
    
    def get_queryset(self):
        workspace_id = self.kwargs.get("workspace_pk")
        return WorkSpaceUser.objects.filter(workspace_id = workspace_id).select_related("user")
    
    
    def perform_create(self, serializer):
        workspace_id = self.kwargs.get("workspace_pk")
        workspace = generics.get_object_or_404(WorkSpace, id=workspace_id)
        
        user = serializer.validated_data.get("user")

        if WorkSpaceUser.objects.filter(
            workspace=workspace,
            user=user
            ).exists():
                raise ValidationError("User already exists in workspace")
        
        serializer.save(workspace = workspace)
        

class WorkSpaceUserDetail(generics.RetrieveUpdateDestroyAPIView):
    
    
    serializer_class = WorkSpaceUserSerializer
    permission_classes = [WorkSpaceUserDetailPermission]
    
    def get_queryset(self):
        workspace_id = self.kwargs.get("workspace_pk")       
        return WorkSpaceUser.objects.filter(workspace_id = workspace_id)


class WorkSpaceList(generics.ListCreateAPIView):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceSerializer
    permission_classes = [WorkSpacePermission]


class WorkSpaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceSerializer
    permission_classes = [WorkSpaceDetailPermission]




class ProjectUserList(generics.ListCreateAPIView):
    serializer_class = ProjectUserSerializer
    permission_classes = [ProjectUserPermission]
    
    def get_queryset(self):
        project_id = self.kwargs.get("project_pk")
        
        return ProjectUser.objects.filter(project_id = project_id).select_related("user")
    

    def perform_create(self, serializer):
        project_id = self.kwargs.get("project_pk")
        project = generics.get_object_or_404(Project, id=project_id)
        
        serializer.save(project = project)
        
        

class ProjectUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectUser.objects.all()
    serializer_class = ProjectUserSerializer
    permission_classes = [ProjectUserDetailPermission]


#ListCreateAPIView: only get and post. Therefore better for a listing and adding.
class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [ProjectListPermission]

    def get_queryset(self):
        workspace_pk = self.kwargs.get('pk')
        return Project.objects.filter(project_of_workspace_id=workspace_pk)

    def perform_create(self, serializer):
        workspace_pk = self.kwargs.get('pk')
        workspace = generics.get_object_or_404(WorkSpace, pk=workspace_pk)
        serializer.save(project_of_workspace=workspace)


#RetrieveUpdateDestroyAPIView: only get, put, patch, delete. Therefore better for a single instance.
class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [ProjectDetailPermission]
    
    def get_queryset(self):
        workspace_pk = self.kwargs.get('workspace_pk')
        return Project.objects.filter(project_of_workspace_id=workspace_pk)
    

class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        workspace_pk = self.kwargs.get('workspace_pk')
        project_pk = self.kwargs.get('project_pk')
        return Task.objects.filter(
            task_of_workspace_id=workspace_pk, 
            task_of_project_id = project_pk
            )

    def perform_create(self, serializer):
        workspace_pk = self.kwargs.get('workspace_pk')
        project_pk = self.kwargs.get('project_pk')
        
        workspace = generics.get_object_or_404(WorkSpace, pk=workspace_pk)
        project = generics.get_object_or_404(Project, pk=project_pk)
        serializer.save(task_of_workspace=workspace, task_of_project=project)
        

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        workspace_pk = self.kwargs.get('workspace_pk')
        project_pk = self.kwargs.get('project_pk')
        return Task.objects.filter(
            task_of_workspace_id=workspace_pk, 
            task_of_project_id = project_pk
            )