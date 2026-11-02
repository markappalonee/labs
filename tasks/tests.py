from django.test import TestCase
from accounts.models import User
from .models import Project, Membership, Task
from .services import transfer_project_ownership

class Lab1ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='alice', email='alice@example.test')
        self.project = Project.objects.create(name='Alpha', owner=self.user)

    def test_duplicate_membership_is_rejected(self):
        Membership.objects.create(user=self.user, project=self.project, role='ADMIN')
        with self.assertRaises(Exception):
            Membership.objects.create(user=self.user, project=self.project, role='MEMBER')

    def test_task_status_choices_exist(self):
        task = Task.objects.create(project=self.project, title='Build API')
        self.assertEqual(task.status, Task.Status.TODO)

    def test_transfer_ownership_updates_project_and_membership(self):
        new_owner = User.objects.create(username='bob', email='bob@example.test')
        transfer_project_ownership(self.project.id, new_owner.id)
        self.project.refresh_from_db()
        self.assertEqual(self.project.owner_id, new_owner.id)
        self.assertEqual(Membership.objects.get(user=new_owner, project=self.project).role, 'ADMIN')
