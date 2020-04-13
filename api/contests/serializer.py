from django.db.models import Max, Sum
from rest_framework import serializers

from .models import Contests, Teams, Tasks, TaskSubmissions, Questions

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
        sum_points = TaskSubmissions.objects.filter(
            team=obj.id).aggregate(
            Sum('point'))["point__sum"]
        return sum_points or 0

    def get_task_index(self, obj):
        sum_points = TaskSubmissions.objects.filter(
            team=obj.id, status="accepted").count()
        return sum_points or 0

    def get_last_submission_time(self, obj):
        last_submission = TaskSubmissions.objects.filter(
            team=obj.id).aggregate(
            Max('date_created'))["date_created__max"]
        return last_submission

class TeamsDetailSerializer(serializers.ModelSerializer):
    contest = serializers.SerializerMethodField()
    submissions = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Teams
        fields = ('id', 'name', 'ip_address', 'vs_liveshare_link', 'github_branch_name',
                  'contest', 'submissions', 'questions')

    def get_contest(self, obj):
        return ContestsDetailSerializer(obj.contest).data

    def get_submissions(self, obj):
        return TaskSubmissionsSerializer(
            TaskSubmissions.objects.all().filter(
                team=obj.id
            ).order_by(
                'date_created'
            ), many=True
        ).data

    def get_questions(self, obj):
        return QuestionsSerializer(
            Questions.objects.all().filter(
                team=obj.id
            ).order_by(
                'date_created'
            ), many=True
        ).data

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'title', 'sub_title', 'text')

class TaskSubmissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSubmissions
        fields = ('id', 'task', 'team', 'status', 'point', 'date_created')

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('id', 'task', 'team', 'text', 'comment', 'link', 'status', 'point', 'date_created')
