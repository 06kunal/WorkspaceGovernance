from rest_framework import serializers

from django.utils import timezone

from company_app.models import WorkSpace, WorkSpaceUser, Project, Task
              
        
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

class WorkSpaceSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    class Meta:
        model = WorkSpace
        fields = "__all__"