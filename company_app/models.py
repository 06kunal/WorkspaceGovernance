from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



# Create your models here.
    
role_choices = [
        ('EMP', 'Employee'),
        ('MNG', 'Manager'),
        ('HOD', 'Head of the department'),
    ]

    
    
class CustomUser(AbstractUser):
    
    ROLE_CHOICES = [
        ('OWN', 'Owner'),
        ('EMP', 'Employee'),
    ]

    role = models.CharField(
        max_length=3,
        choices=ROLE_CHOICES,
        default='EMP'
    )
    
        
class WorkSpace(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    

class WorkSpaceUser(models.Model):
    
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="workspaceuser")
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

    
class ProjectUser(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projectuser")
    role = models.CharField(max_length=10, choices=role_choices, default='EMP')
    
    
    class Meta:
        unique_together = ('user', 'project')
        
        
    def __str__(self):
        return f"{self.user.username} -> {self.project.project_name} - ({self.role})"
    
    

class Task(models.Model):
    
    status_choices = [
        ('PND', 'Pending'),
        ('RES', 'Resolved'),
        ('AWT', 'Awaiting response'),
    ]
    priority_choices = [
        ('LOW', 'Not so Important'),
        ('MDM', 'Important'),
        ('HGH', 'Immediate attention'),
    ]
    
    task_name = models.CharField(max_length=50)
    task_description = models.CharField(max_length=500)
    task_of_workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="taskworkspace")
    task_of_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_tasks")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks_received")
    status = models.CharField(max_length=3, choices=status_choices, default= 'PND')
    priority = models.CharField(max_length=3, choices=priority_choices, default= 'Low')
    completion_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.task_name} -> {self.task_of_project}"
    
    
    
    
