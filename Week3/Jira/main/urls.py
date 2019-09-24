from django.urls import path
from main.views import ProjectListCreate, ProjectRetrieveUpdateDelete, BlockViewSet
from rest_framework import routers

urlpatterns = [
    path('projects/', ProjectListCreate.as_view()),
    path('projects/<int:pk>/', ProjectRetrieveUpdateDelete.as_view())
]

router = routers.DefaultRouter()
router.register('blocks', BlockViewSet, basename='main')

urlpatterns += router.urls