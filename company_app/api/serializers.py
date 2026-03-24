from rest_framework import serializers

from django.utils import timezone

from company_app.models import WorkSpace, WorkSpaceUser, Project, Task, ProjectUser
              
        
class TaskSerializer(serializers.ModelSerializer):
    # return the name of the related workspace in responses
    workspace_name = serializers.CharField(source='task_of_workspace.name', read_only=True)
    project_name = serializers.CharField(source='task_of_project.name', read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "task_name",
            "task_description",
            "task_of_workspace",
            "task_of_project",
            "workspace_name",
            "project_name",
            "status",
            "priority",
            "active",
            "created",
            "completion_date",
        ]
        extra_kwargs = {
            # workspace is supplied by the view (URL argument) so we don't expect
            # it in the request body
            "task_of_workspace": {"write_only": True, "required": False},
            "task_of_project": {"write_only": True, "required": False},
        }
        
    def update(self, instance, validated_data):
        print(validated_data)
        new_status = validated_data.get("status", instance.status)

        # Case 1: task becomes resolved
        if new_status == "RES" and instance.status != "RES":
            validated_data["completion_date"] = timezone.now()

        # Case 2: task moves from resolved to another status
        elif instance.status == "RES" and new_status != "RES":
            validated_data["completion_date"] = None

        return super().update(instance, validated_data)

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    # return the name of the related workspace in responses
    workspace_name = serializers.CharField(source='project_of_workspace.name', read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "project_name",
            "project_description",
            "project_of_workspace",
            "workspace_name",
            "active",
            "created",
            "tasks",
        ]
        extra_kwargs = {
            # workspace is supplied by the view (URL argument) so we don't expect
            # it in the request body
            "project_of_workspace": {"write_only": True, "required": False},
        }


class ProjectUserSerializer(serializers.ModelSerializer):
    project = serializers.CharField(source="project.project_name", read_only = True)
    username = serializers.CharField(source = "user.username", read_only = True)
    
    class Meta:
        model = ProjectUser
        fields = "__all__"
        extra_kwargs = {
            "user": {"write_only": True}
        }



class WorkSpaceSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkSpace
        fields = "__all__"
        
    def get_projects(self, obj):
        
        user = self.context["request"].user
        
        ws_user = WorkSpaceUser.objects.filter(
            workspace = obj,
            user = user
        ).only("role").first()
        
        current_role = ws_user.role if ws_user else None
        
        
        
        #Owner, superuser and the hod should see all the projects
        if getattr(user, "role", None) == "OWN" or user.is_superuser or current_role == "HOD":
            return ProjectSerializer(obj.projects.all(), many=True, read_only = True).data
        
        # MNG / EMP → only their projects
        return ProjectSerializer(
            obj.projects.filter(
                members__user=user
            ).distinct(),
            many=True,
            read_only = True
        ).data        
         

class WorkSpaceUserSerializer(serializers.ModelSerializer):
    workspace = serializers.CharField(source='workspace.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    
    class Meta:
        model = WorkSpaceUser
        fields = "__all__"
        extra_kwargs = {
            "user": {"write_only": True}
        }