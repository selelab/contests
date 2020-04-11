import django_filters
from django.shortcuts import render
from rest_framework import filters, permissions, viewsets

from web import settings

from .models import Contests, Teams, Tasks
from .serializer import ContestsSerializer, TeamsSerializer, TasksSerializer


class ListContestsViewSet(viewsets.ModelViewSet):
    serializer_class = ContestsSerializer
    queryset = Contests.objects.all()

class ListTeamsViewSet(viewsets.ModelViewSet):
    serializer_class = TeamsSerializer
    queryset = Teams.objects.all()

class ListTasksViewSet(viewsets.ModelViewSet):
    serializer_class = TasksSerializer
    queryset = Tasks.objects.all()
