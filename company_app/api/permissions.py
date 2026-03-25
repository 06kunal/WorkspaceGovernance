from rest_framework.permissions import BasePermission, SAFE_METHODS
from company_app.models import WorkSpaceUser, ProjectUser, WorkSpace, Project



#Helper functions
def get_workspace_role(user, workspace):
    ws_user = WorkSpaceUser.objects.filter(
        workspace = workspace,
        user = user
    ).only("role").first()
    
    return ws_user.role if ws_user else None


def is_admin(user):
    return getattr(user, "role", None) == "OWN" or user.is_superuser
    

def is_workspace_user(user, workspace):
    return WorkSpaceUser.objects.filter(
        workspace = workspace,
        user = user
    ).exists()
    
def is_project_user(user, project):
    return ProjectUser.objects.filter(
        project = project,
        user = user
    ).exists()


# Permission class for get and post workspaceuserlist.
class WorkSpaceUserPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        workspace_id = view.kwargs.get("workspace_pk")
        workspace = WorkSpace.objects.filter(id=workspace_id).first()
        if not workspace:
            return False

        # SUPERUSER amd owner→ full access
        if is_admin(user):
            return True

        # Get workspace role
        current_role = get_workspace_role(user, workspace)

        if not current_role:
            return False


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

        workspace = obj.workspace
        
        if not is_workspace_user(user, workspace):
            return False
        
        current_role = get_workspace_role(user, workspace)


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
        workspace = WorkSpace.objects.filter(id=workspace_id).first()
        if not workspace:
            return False
        
        project_id = view.kwargs.get("project_pk")
        project = Project.objects.filter(id=project_id).first()
        if not project:
            return False
        
        # Ensuring project belongs to a workspace
        if project.project_of_workspace_id != workspace.id:
            return False

        # get role
        current_role = get_workspace_role(user, workspace)
        if not current_role:
            return False
        
        # HOD→ full access
        if current_role == "HOD":
            return True
        
        is_proj_user = is_project_user(user, project)
        
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            
            if current_role in ["MNG", "EMP"]:
                return is_proj_user
            
            return False
        
        if request.method == "POST":
            
            if current_role == "MNG":
                
                if not is_proj_user:
                    return False
                
                role_to_assign = request.data.get("role")

                return role_to_assign in ["DEV", "QA", "TST"]
        
        return False

        
        

# Permission class for ProjectUserDetail
# The Manger and Emp could only see a user if it is from his own project. 
class ProjectUserDetailPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Get workspace role
        workspace = obj.project.project_of_workspace        
        current_role = get_workspace_role(user, workspace)
        
        # SUPERUSER and HOD → full access
        if is_admin(user) or current_role == "HOD":
            return True


        # SAFE METHODS (GET, HEAD, OPTIONS)
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            
            if current_role in ["MNG", "EMP"]:
                return is_project_user(user, obj.project)
        
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
        workspace = WorkSpace.objects.get(id= workspace_id)
        if not workspace:
            return False
        
        current_role = get_workspace_role(user, workspace)
        
        return current_role == "HOD"
    
 
 
    
# Permission class for ProjectDetail view. This view accepts GET, PUT, PATCH and DELETE requests
# MNG and EMP could only see only their project. 
# Admin and HOD can do whatever they want to do with the project.
class ProjectDetailPermission(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        user = request.user        
        
        workspace = obj.project_of_workspace
        if not workspace:
            return False
        
        current_role = get_workspace_role(user, workspace)
        
        # Admin and HOD the allow everything
        if is_admin(user) or current_role == "HOD":
            return True
        
        if request.method in SAFE_METHODS:
            
            if current_role in ["EMP", "MNG"]:
                return is_project_user(user, obj)
            
            return False
        
        return False
            
            
            
    
       
        
        