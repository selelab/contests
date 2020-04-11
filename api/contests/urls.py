from rest_framework import routers

from .views import ListContestsViewSet, ListTeamsViewSet, ListTasksViewSet

router = routers.DefaultRouter()
router.register(r'contests', ListContestsViewSet)
router.register(r'teams', ListTeamsViewSet)
router.register(r'tasks', ListTasksViewSet)
