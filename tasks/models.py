from django.db import models
from django.core.validators import MinLengthValidator
from accounts.models import User
class Project(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    owner=models.ForeignKey(User,on_delete=models.PROTECT,db_column='owner_id')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='lab_projects'
        indexes = [models.Index(fields=['owner'])]
class Membership(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_column='user_id')
    project=models.ForeignKey(Project,on_delete=models.CASCADE,db_column='project_id')
    role=models.CharField(max_length=10)
    class Meta:
        db_table='lab_memberships'
        constraints = [models.UniqueConstraint(fields=['user','project'], name='uq_membership_user_project')]
        indexes = [models.Index(fields=['project','role'])]
class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'TODO', 'To do'
        PROGRESS = 'PROGRESS', 'In progress'
        DONE = 'DONE', 'Done'
    project=models.ForeignKey(Project,on_delete=models.CASCADE,db_column='project_id')
    assigned_to=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,db_column='assigned_to')
    title=models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    description=models.TextField(blank=True)
    status=models.CharField(max_length=10, choices=Status.choices, default=Status.TODO)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='lab_tasks'
        indexes = [models.Index(fields=['project','status']), models.Index(fields=['assigned_to','status'])]
