from rest_framework.permissions import BasePermission
from company_app.models import WorkSpaceUser


class CanCreateUser(BasePermission):

    def has_permission(self, request, view):

        workspace_id = view.kwargs.get("workspace_id")

        role = WorkSpaceUser.objects.filter(
            user=request.user,
            workspace_id=workspace_id
        ).values_list("role", flat=True).first()

        new_role = request.data.get("role")

        if role == "OWN":
            return True

        if role == "HOD" and new_role in ["MNG", "EMP"]:
            return True

        if role == "MNG" and new_role == "EMP":
            return True

        return False