from django.db.models import Count, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, Task, Membership, User
from .permissions import ProjectMember, ProjectAdmin
from .serializers import ProjectSerializer, TaskSerializer

def member_projects(user):
    return Project.objects.filter(membership__user__username=user.username).distinct()

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    def get_queryset(self): return member_projects(self.request.user).annotate(total=Count('task', distinct=True))
    def perform_create(self, serializer):
        owner, _ = User.objects.get_or_create(
            username=self.request.user.username,
            defaults={'email': f'{self.request.user.username}@example.com'},
        )
        project = serializer.save(owner=owner)
        Membership.objects.create(user=owner, project=project, role='ADMIN')
    def get_permissions(self): return [ProjectAdmin()] if self.action in ['destroy','update','partial_update'] else [ProjectMember()]
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        p = self.get_object(); qs = p.task_set.all()
        total = qs.count(); done = qs.filter(status='DONE').count()
        return Response({'total':total, 'todo':qs.filter(status='TODO').count(), 'progress':qs.filter(status='PROGRESS').count(), 'done':done, 'completion_rate': round(done * 100 / total, 2) if total else 0})

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    def get_queryset(self):
        qs = Task.objects.filter(project__in=member_projects(self.request.user)).select_related('project','assigned_to')
        for field in ['status','project_id','assigned_to_id']:
            if self.request.query_params.get(field): qs = qs.filter(**{field:self.request.query_params[field]})
        return qs.order_by('-created_at')
    def get_permissions(self): return [ProjectAdmin()] if self.action == 'destroy' else [ProjectMember()]
