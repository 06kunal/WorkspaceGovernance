from rest_framework.permissions import BasePermission
from company_app.models import WorkSpaceUser, ProjectUser


# Permission class for get and post workspaceuserlist.
class WorkSpaceUserPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        workspace_id = view.kwargs.get("workspace_pk")

        # SUPERUSER → full access
        if user.is_superuser:
            return True

        # OWNER → full access
        if getattr(user, "role", None) == "OWNER":
            return True

        # Get workspace role
        ws_user = WorkSpaceUser.objects.filter(
            workspace_id=workspace_id,
            user=user
        ).first()

        if not ws_user:
            return False

        current_role = ws_user.role


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
        if user.is_superuser:
            return True

        # OWNER → full access
        if getattr(user, "role", None) == "OWNER":
            return True

        # Get workspace role
        ws_user = WorkSpaceUser.objects.filter(
            workspace=obj.workspace,
            user=user
        ).first()

        if not ws_user:
            return False

        current_role = ws_user.role


        # SAFE METHODS (GET, HEAD, OPTIONS)
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return current_role in ["HOD", "MNG", "EMP"]


        # WRITE METHODS
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return current_role == "HOD"

        return False
    
    
    
    

# Permission class for ProjectUserList. Get and Post Method
# HOD can get all the project users and add a new user to a project.
# MNG can add a user to his own project in any role(QA, tester, developer) 
class ProjectUserPermission(BasePermission):
    
    def has_permission(self, request, view):
        
        user = request.user
        workspace_id = view.kwargs.get("workspace_pk")
        project_id = view.kwargs.get("project_pk")
        
        # Superuser -> full access
        if user.is_superuser:
            return True
        
        # Owner -> full access
        if getattr(user, "role", None) == "OWN":
            return True
        
        ws_user = WorkSpaceUser.objects.filter(
            workspace_id = workspace_id,
            user = user
        ).first()
        
        
        
        if not ws_user:
            return False
        
        
        current_role = ws_user.role
        
        if request.method == "GET":
            return current_role == "HOD"
        
        if request.method == "POST":
            if current_role == "HOD":
                return True
            
            if current_role == "MNG":
                project_user = ProjectUser.objects.filter(
                    project_id = project_id,
                    user = user
                ).exists()
                
                if not project_user:
                    return False
                
                role_to_assign = request.data.get("role")

                return role_to_assign in ["DEV", "QA", "TST"]
        
        return False

        