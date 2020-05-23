from django.db.models import Max, Sum
from rest_framework import serializers

from datetime import datetime

from .models import (
    Contests,
    Teams,
    Tasks,
    TaskSubmissions,
    Questions,
    ContestsTasks,
    Hints,
    DataSets
)

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
    id = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    task_index = serializers.SerializerMethodField()
    last_submission_time = serializers.SerializerMethodField()

    class Meta:
        model = Teams
        fields = ('id', 'name', 'points', 'task_index', 'last_submission_time')

    def get_id(self, obj):
        now = datetime.now()
        if (obj.contest.end.second > now.second):
            return obj.id
        else:
            return None

    def get_points(self, obj):
        submissions = TaskSubmissionsSerializer(
            TaskSubmissions.objects.filter(
                team=obj.id
            ).order_by(
                'date_created'
            ), many=True
        ).data

        point = 0
        for submission in submissions:
            if (submission["point"]):
                sum_points_used = Questions.objects.filter(
                    team=obj.id, task=submission["task"]).aggregate(
                    Sum('point'))["point__sum"]
                point += max(0, submission["point"] - (sum_points_used or 0))

        return point

    def get_task_index(self, obj):
        sum_points = TaskSubmissions.objects.filter(
            team=obj.id, status="accepted").count()
        return sum_points or 0

    def get_last_submission_time(self, obj):
        last_submission = TaskSubmissions.objects.filter(
            team=obj.id).aggregate(
            Max('date_created'))["date_created__max"]
        return last_submission

class CreateTeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ('id', 'name', 'ip_address', 'vs_liveshare_link', 'github_branch_name', 'contest')

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
            TaskSubmissions.objects.filter(
                team=obj.id
            ).order_by(
                'date_created'
            ), many=True
        ).data

    def get_questions(self, obj):
        return QuestionsSerializer(
            Questions.objects.filter(
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
        fields = ('id', 'task', 'team', 'title', 'text', 'comment', 'link', 'status', 'point', 'date_created')

class ContestsTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestsTasks
        fields = ('task', 'contest', 'ordering')

class HintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hints
        fields = ('id', 'task', 'text', 'date_created')


class DataSetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSets
        fields = ('id', 'title', 'json_data')
