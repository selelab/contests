from rest_framework import routers

from .views import (
    ListContestsViewSet,
    ListTeamsViewSet,
    ListTasksViewSet,
    TaskSubmissionsViewSet,
    QuestionsViewSet,
    ContestsTasksViewSet,
    HintsViewSet,
    DataSetsViewSet
)

router = routers.DefaultRouter()
router.register(r'contests', ListContestsViewSet)
router.register(r'teams', ListTeamsViewSet)
router.register(r'tasks', ListTasksViewSet)
router.register(r'submissions', TaskSubmissionsViewSet)
router.register(r'questions', QuestionsViewSet)
router.register(r'task-ordering', ContestsTasksViewSet)
router.register(r'hints', HintsViewSet)
router.register(r'data-sets', DataSetsViewSet)
