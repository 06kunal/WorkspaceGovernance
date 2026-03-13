from rest_framework import generics

from company_app.models import WorkSpace, WorkSpaceUser, Project, Task
from company_app.api.serializers import WorkSpaceSerializer, ProjectSerializer, TaskSerializer


class WorkSpaceList(generics.ListCreateAPIView):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceSerializer


class WorkSpaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceSerializer

#ListCreateAPIView: only get and post. Therefore better for a list and adding.
class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

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