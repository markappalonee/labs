from django.db import models
from accounts.models import User
class Project(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    owner=models.ForeignKey(User,on_delete=models.PROTECT,db_column='owner_id')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='lab.projects'
        managed=False
class Membership(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_column='user_id')
    project=models.ForeignKey(Project,on_delete=models.CASCADE,db_column='project_id')
    role=models.CharField(max_length=10)
    class Meta:
        db_table='lab.memberships'
        managed=False
class Task(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,db_column='project_id')
    assigned_to=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,db_column='assigned_to')
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    status=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='lab.tasks'
        managed=False
