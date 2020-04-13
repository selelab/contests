import django_filters
from django.shortcuts import render
from rest_framework import filters, permissions, viewsets

from web import settings

from .models import Contests, Teams, Tasks, TaskSubmissions, Questions
from .serializer import ContestsSerializer, TeamsSerializer, TeamsDetailSerializer, TasksSerializer, TaskSubmissionsSerializer, QuestionsSerializer


class ListContestsViewSet(viewsets.ModelViewSet):
    serializer_class = ContestsSerializer
    queryset = Contests.objects.all()

class ListTeamsViewSet(viewsets.ModelViewSet):
    serializer_class = TeamsSerializer
    queryset = Teams.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeamsDetailSerializer
        return self.serializer_class

class ListTasksViewSet(viewsets.ModelViewSet):
    serializer_class = TasksSerializer
    queryset = Tasks.objects.all()

class TaskSubmissionsViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSubmissionsSerializer
    queryset = TaskSubmissions.objects.all()

    def get_queryset(self):
        team = self.request.GET.get('team')
        if team:
            return TaskSubmissions.objects.filter(team=team)
        else:
            return self.queryset

class QuestionsViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionsSerializer
    queryset = Questions.objects.all()

    def get_queryset(self):
        team = self.request.GET.get('team')
        if team:
            return Questions.objects.filter(team=team)
        else:
            return self.queryset
