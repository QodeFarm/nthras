from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

#add your urls

router = DefaultRouter()

router.register(r'tasks', TasksViewSet)
router.register(r'task_comments', TaskCommentsViewSet)
router.register(r'task_attachments', TaskAttachmentsViewSet)
router.register(r'task_history', TaskHistoryViewSet)

urlpatterns = [
    path('',include(router.urls))
]