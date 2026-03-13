from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    

    
class WorkSpace(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    

class WorkSpaceUser(models.Model):
    
    role_choices = [
        ('EMP', 'Employee'),
        ('MNG', 'Manager'),
        ('HOD', 'Head of the department'),
    ]
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="workspace")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workspaceuser")
    role = models.CharField(max_length=3, choices=role_choices, default= 'EMP')
    
    
    # so that there could not be multiple enries of a same user.
    class Meta:
        unique_together = ('user', 'workspace')
    

    def __str__(self):
        return f"{self.user.username} -> {self.workspace.name} - ({self.role})"
    
    

class Project(models.Model):
    project_name = models.CharField(max_length=50)
    project_description = models.CharField(max_length=500)
    project_of_workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="projects")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.project_name} | {self.project_of_workspace}"

    

class Task(models.Model):
    
    status_choices = [
        ('PND', 'Pending'),
        ('RES', 'Resolved'),
        ('AWT', 'Awaiting response'),
    ]
    priority_choices = [
        ('3', 'Not so Important'),
        ('2', 'Important'),
        ('1', 'Immediate attention'),
    ]
    
    task_name = models.CharField(max_length=50)
    task_description = models.CharField(max_length=500)
    task_of_workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="taskworkspace")
    task_of_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    # assigned_by = models.ForeignKey(User, )
    # assigned_to = models.ForeignKey(User, )
    status = models.CharField(max_length=3, choices=status_choices, default= 'PND')
    priority = models.CharField(max_length=3, choices=priority_choices, default= '3')
    completion_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.task_name} -> {self.task_of_project}"
