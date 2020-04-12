from django.db.models import Sum
from rest_framework import serializers

from .models import Contests, Teams, Tasks

class ContestsSerializer(serializers.ModelSerializer):
    teams = serializers.SerializerMethodField()

    class Meta:
        model = Contests
        fields = ('id', 'title', 'start', 'end', 'tasks', 'teams')

    def get_teams(self, obj):
        try:
            team_abstruct_contents = TeamsSerializer(Teams.objects.all().filter(contest=Contests.objects.get(id=obj.id)), many=True).data
            return team_abstruct_contents
        except:
            team_abstruct_contents = None
            return team_abstruct_contents

class ContestsDetailSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Contests
        fields = ('id', 'title', 'start', 'end', 'tasks')

    def get_tasks(self, obj):
        return TasksSerializer(obj.tasks.order_by('conteststasks'), many=True).data
class TeamsSerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField()
    task_index = serializers.SerializerMethodField()
    last_submission_time = serializers.SerializerMethodField()

    class Meta:
        model = Teams
        fields = ('id', 'name', 'points', 'task_index', 'last_submission_time')

    def get_points(self, obj):
        return 10

    def get_task_index(self, obj):
        return 2

    def get_last_submission_time(self, obj):
        return "0:31"

class TeamsDetailSerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField()
    task_index = serializers.SerializerMethodField()
    last_submission_time = serializers.SerializerMethodField()
    contest = serializers.SerializerMethodField()

    class Meta:
        model = Teams
        fields = ('id', 'name', 'ip_address', 'vs_liveshare_link', 'github_branch_name', 'contest', 'points', 'task_index', 'last_submission_time', 'submissions')

    def get_points(self, obj):
        return 10

    def get_task_index(self, obj):
        return 2

    def get_last_submission_time(self, obj):
        return "0:31"

    def get_contest(self, obj):
        return ContestsDetailSerializer(obj.contest).data

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'title', 'sub_title', 'text')
