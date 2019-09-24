from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from main.serializers import ProjectSerializer, BlockSerializer, TaskSerializer, TaskCommentSerializer, TaskDocumentSerializer
from main.models import Project, Block, Task, TaskComment, TaskDocument
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action


class ProjectListCreate(APIView):
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post']

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['creator'] = request.user.id
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

class ProjectRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'put', 'patch', 'delete']
    permission_classes = (IsAuthenticated, )
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def perform_update(self, instance):
        if self.request.user == self.get_object().creator:
            instance.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        if self.request.user == self.get_object().creator:
            instance.delete()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class BlockViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    permission_classes = (IsAuthenticated, )

    def perform_update(self, instance):
        if self.request.user == self.get_object().project.creator:
            instance.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        if self.request.user == self.get_object().project.creator:
            instance.delete()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class TaskViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, )


class TaskCommentViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = (IsAuthenticated, )

class TaskDocumentViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = TaskDocument.objects.all()
    serializer_class = TaskDocumentSerializer
    permission_classes = (IsAuthenticated, )