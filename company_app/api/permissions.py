from rest_framework.exceptions import NotFound,  PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS
from company_app.models import WorkSpaceUser, ProjectUser, WorkSpace, Project



#Helper functions

def get_workspace_role(user, workspace_id):
    workspace = WorkSpace.objects.filter(id = workspace_id).first()    
    if not workspace:
        raise NotFound(f"Workspce with id {workspace_id} does not exist.")
        
    ws_user = WorkSpaceUser.objects.filter(workspace = workspace, user = user).first()    
    if not ws_user:
        raise PermissionDenied("User is not part of this workspace.")
    
    return ws_user.role

def is_workspace_user(user, workspace):    
    ws_user = WorkSpaceUser.objects.filter(workspace = workspace, user = user).exists()
    if not ws_user:
        raise PermissionDenied("User is not part of this workspace.")
    return ws_user
    

def is_admin(user):
    return getattr(user, "role", None) == "OWN" or user.is_superuser
    
    
def is_project_user(user, project_id):
    project = Project.objects.filter(id = project_id).first()
    if not project:
        raise NotFound(f"Project with id {project_id} does not exist.")
    
    pj_user = ProjectUser.objects.filter(
        project = project,
        user = user
    ).exists()
    
    if not pj_user:
        raise PermissionDenied("User is not part of this project.")
    
    return pj_user


# Permission class for get and post workspaceuserlist.
class WorkSpaceUserPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        
        # SUPERUSER amd owner→ full access
        if is_admin(user):
            return True
        
        # Get workspace role
        workspace_id = view.kwargs.get("workspace_pk") 
        current_role = get_workspace_role(user, workspace_id)

        # GET (LIST) restriction
        if request.method == "GET":
            return current_role == "HOD"


        # POST (CREATE) logic
        if request.method == "POST":
            role_to_assign = request.data.get("role")

            if not role_to_assign:
                return False

            if current_role == "HOD":
                return role_to_assign in ["MNG", "EMP"]

            if current_role == "MNG":
                return role_to_assign == "EMP"

            return False

        return False
    
    
    
# Permission class for workspaceuserdetail. 
class WorkSpaceUserDetailPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        # SUPERUSER → full access
        if is_admin(user):
            return True

        # Get workspace role
        workspace_id = view.kwargs.get("workspace_pk") 
        current_role = get_workspace_role(user, workspace_id)


        # SAFE METHODS (GET, HEAD, OPTIONS)
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return current_role in ["HOD", "MNG", "EMP"]


        # WRITE METHODS
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return current_role == "HOD"

        return False
    
    


# Permission class for Workspace
# only owner and superuser can create a workspace. 
class WorkSpacePermission(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        
        # OWNER and superuser → full access
        return is_admin(user)
       
        

# only owner and superuser can do anything but if the user is part of the workspace then he can only view his own workspace.
class WorkSpaceDetailPermission(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # SUPERUSER amd owner→ full access
        if is_admin(user):
            return True
        
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return is_workspace_user(user, obj)
        
        return False
        
        
    

    

# Permission class for ProjectUserList. Get and Post Method
# HOD can get all the project users and add a new user to a project.
# MNG can add a user to his own project in any role(QA, tester, developer) 
class ProjectUserPermission(BasePermission):
    
    def has_permission(self, request, view):
        
        user = request.user
        
        #Ower-> full access
        if is_admin(user):
            return True
        
        workspace_id = view.kwargs.get("workspace_pk")        
        project_id = view.kwargs.get("project_pk")
        
        # get role
        current_role = get_workspace_role(user, workspace_id)

        
        # HOD→ full access
        if current_role == "HOD":
            return True
        
        is_proj_user = is_project_user(user, project_id)
        
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            
            if current_role in ["MNG", "EMP"]:
                return is_proj_user
            
            return False
        
        if request.method == "POST":
            
            if current_role == "MNG":
                role_to_assign = request.data.get("role")

                return role_to_assign in ["DEV", "QA", "TST"]
        
        return False

        
        

# Permission class for ProjectUserDetail
# The Manger and Emp could only see a user if it is from his own project. 
class ProjectUserDetailPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if is_admin(user):
            return True 

        # Get workspace role
        workspace_id = view.kwargs.get("workspace_pk")         
        current_role = get_workspace_role(user, workspace_id)
        
        # HOD → full access
        if current_role == "HOD":
            return True


        # SAFE METHODS (GET, HEAD, OPTIONS)
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            
            if current_role in ["MNG", "EMP"]:
                return is_project_user(user, view.kwargs.get("project_pk"))
        
            return False

        return False
    
    
    
# Permission class of ProjectList view. this view only contains Get and Post method.
# Only admin, HOD should get the access for adding the project i.e to POST request. 
# MNG and EMP should not get the list of all the projects.
class ProjectListPermission(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        
        # if the user is admin then allow.
        if is_admin(user):
            return True
        
        workspace_id = view.kwargs.get("pk")        
        current_role = get_workspace_role(user, workspace_id)
        
        return current_role == "HOD"
    
 
 
    
# Permission class for ProjectDetail view. This view accepts GET, PUT, PATCH and DELETE requests
# MNG and EMP could only see only their project. 
# Admin and HOD can do whatever they want to do with the project.
class ProjectDetailPermission(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        user = request.user   
        
        if is_admin(user):
            return True     
        
        workspace_id = obj.project_of_workspace.id    
        current_role = get_workspace_role(user, workspace_id)
        
        # HOD the allow everything
        if current_role == "HOD":
            return True
        
        if request.method in SAFE_METHODS:
            
            if current_role in ["EMP", "MNG"]:
                return is_project_user(user, view.kwargs.get("pk"))
                        
            return False
        
        return False
            
            
            
    
#Permission class for TaskList view. 
# everybody can create a task except the emp.
# everyone can view the task.
class TaskListPermission(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        
        if is_admin(user):
            return True
        
        workspace_id = view.kwargs.get("workspace_pk")
        current_role = get_workspace_role(user, workspace_id)
        
        if current_role == "HOD":
            return True
        
        project_id = view.kwargs.get("project_pk")
        is_proj_user = is_project_user(user, project_id)
        
        if current_role == "MNG":
            return is_proj_user
        
        if request.method in SAFE_METHODS:
            return is_proj_user
        
        return False
    
    

# Permission class for TaskDetail view.
# everyone can access the detail, but the emp could only send the patch request and that too only for the status part and that too only that emp who has the task assigned.
class TaskDetailPermission(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        user = request.user 
        
        if is_admin(user):
            return True
        
        workspace_id = obj.task_of_workspace.id
        current_role = get_workspace_role(user, workspace_id)
        
        if current_role == "HOD":
            return True
        
        project_id = obj.task_of_project.id
        is_proj_user = is_project_user(user, project_id)
        
        if current_role == "MNG":
            return is_proj_user
        
        if request.method in SAFE_METHODS:
            return is_proj_user
        
        if current_role == "EMP":
            if request.method == "PATCH" and user == obj.assigned_to:
                incoming_fields = set(request.data.keys())               
                return incoming_fields == {"status"}
            return False
            
        return False
            
            
                
        
          
        
       
        
        