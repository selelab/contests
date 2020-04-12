import uuid

from django.db import models
from django import utils

class Contests(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    tasks = models.ManyToManyField("Tasks", through="ContestsTasks")

    class Meta:
        db_table = "contests"

class Teams(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=15)
    vs_liveshare_link = models.CharField(max_length=2048)
    github_branch_name = models.CharField(max_length=50)
    contest = models.ForeignKey(Contests, on_delete=models.CASCADE)
    submissions = models.ManyToManyField("Tasks", through="TaskSubmissions")

    class Meta:
        db_table = "teams"
        ordering = ['id']

class Tasks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=50)
    text = models.CharField(max_length=2048)

    class Meta:
        db_table = "tasks"
        ordering = ['id']

class ContestsTasks(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contests, on_delete=models.CASCADE)
    ordering = models.IntegerField()

    class Meta:
        db_table = "contests_tasks_ordering"
        ordering = ['contest', 'ordering']

class TaskSubmissions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="pending")
    point = models.IntegerField(default=0)
    date_created = models.DateTimeField(default=utils.timezone.now, editable=False)
    class Meta:
        db_table = "submissions"
        ordering = ['-date_created', 'id']
