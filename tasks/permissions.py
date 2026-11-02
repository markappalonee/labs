from rest_framework.permissions import BasePermission
from .models import Membership
class ProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        project = getattr(obj, 'project', obj)
        return Membership.objects.filter(project=project, user__username=request.user.username).exists()
class ProjectAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        project = getattr(obj, 'project', obj)
        return Membership.objects.filter(project=project, user__username=request.user.username, role='ADMIN').exists()
