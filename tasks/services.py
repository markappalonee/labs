from django.db import transaction
from .models import Project, Membership, User
def transfer_project_ownership(project_id, new_owner_id):
    with transaction.atomic():
        project = Project.objects.select_for_update().get(pk=project_id)
        new_owner = User.objects.get(pk=new_owner_id)
        project.owner_id = new_owner.id
        project.save(update_fields=['owner'])
        Membership.objects.update_or_create(user=new_owner, project=project, defaults={'role':'ADMIN'})
        return project
