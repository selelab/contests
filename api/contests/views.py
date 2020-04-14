import django_filters
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import filters, permissions, viewsets

from web import settings

from .models import (
    Contests,
    Teams,
    Tasks,
    TaskSubmissions,
    Questions,
    ContestsTasks,
    Hints
)
from .serializer import (
    ContestsSerializer,
    TeamsSerializer,
    CreateTeamsSerializer,
    TeamsDetailSerializer,
    TasksSerializer,
    TaskSubmissionsSerializer,
    QuestionsSerializer,
    ContestsTasksSerializer,
    HintsSerializer
)


class ListContestsViewSet(viewsets.ModelViewSet):
    http_method_names = settings.DEFAULT_HTTP_METHOD_NAMES
    serializer_class = ContestsSerializer
    queryset = Contests.objects.all()

class ListTeamsViewSet(viewsets.ModelViewSet):
    http_method_names = settings.DEFAULT_HTTP_METHOD_NAMES
    serializer_class = TeamsSerializer
    queryset = Teams.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeamsDetailSerializer
        elif self.action == 'create':
            return CreateTeamsSerializer
        return self.serializer_class

    def list(self, request):
        return JsonResponse({'error': 'forbidden'}, status=403)


class ListTasksViewSet(viewsets.ModelViewSet):
    http_method_names = settings.DEFAULT_HTTP_METHOD_NAMES
    serializer_class = TasksSerializer
    queryset = Tasks.objects.all()

class TaskSubmissionsViewSet(viewsets.ModelViewSet):
    http_method_names = settings.DEFAULT_HTTP_METHOD_NAMES
    serializer_class = TaskSubmissionsSerializer
    queryset = TaskSubmissions.objects.all()

    def get_queryset(self):
        team = self.request.GET.get('team')
        if team:
            return TaskSubmissions.objects.filter(team=team)
        else:
            return self.queryset

class QuestionsViewSet(viewsets.ModelViewSet):
    http_method_names = settings.DEFAULT_HTTP_METHOD_NAMES
    serializer_class = QuestionsSerializer
    queryset = Questions.objects.all()

    def list(self, request):
        queryset = Questions.objects.filter(task__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

class ContestsTasksViewSet(viewsets.ModelViewSet):
    http_method_names = settings.DEFAULT_HTTP_METHOD_NAMES
    serializer_class = ContestsTasksSerializer
    queryset = ContestsTasks.objects.all()

class HintsViewSet(viewsets.ModelViewSet):
    http_method_names = settings.DEFAULT_HTTP_METHOD_NAMES
    serializer_class = HintsSerializer
    queryset = Hints.objects.all()

    def list(self, request):
        return JsonResponse({'error': 'forbidden'}, status=403)
