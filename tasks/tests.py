from django.test import TestCase
from accounts.models import User
from .models import Project, Membership, Task

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
