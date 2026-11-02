from rest_framework import serializers
from .models import Project, Membership, Task

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id','name','description','owner','created_at']
        read_only_fields = ['owner']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','project','assigned_to','title','description','status','created_at']
        read_only_fields = ['created_at']
    def validate_title(self, value):
        value = value.strip()
        if len(value) < 3: raise serializers.ValidationError('название должно содержать минимум 3 символа')
        return value
    def validate(self, attrs):
        request = self.context.get('request')
        project = attrs.get('project') or getattr(self.instance, 'project', None)
        assignee = attrs.get('assigned_to', getattr(self.instance, 'assigned_to', None))
        if project and assignee and not Membership.objects.filter(project=project, user=assignee).exists():
            raise serializers.ValidationError({'assigned_to':'пользователь должен быть участником проекта'})
        if request and project and not Membership.objects.filter(project=project, user__username=request.user.username).exists():
            raise serializers.ValidationError({'project':'проект недоступен пользователю'})
        return attrs
