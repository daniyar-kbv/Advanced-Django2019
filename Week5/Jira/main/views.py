from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from main.serializers import ProjectCreateSerializer, TaskSerializer, BlockDetailSerializer, TaskCommentSerializer, \
    TaskDocumentSerializer, ProjectDetailedSerializer, ProjectListSerializer, BlockListSerializer, \
    BlockCreateSerializer, TaskListSerializer, TaskCreateSerializer, TaskCommentListSerializer, \
    TaskDocumentListSerializer
from main.models import Project, Block, Task, TaskComment, TaskDocument
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from main.permissions import IsOwner, BlockPermission, TaskPermission, TaskInsidePermission


class ProjectListCreate(APIView):
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post']

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)


class ProjectViewSet(mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    http_method_names = ['get', 'post']
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailedSerializer
        return ProjectListSerializer

    @action(methods=['GET'], detail=True)
    def tasks(self, request, pk):
        instance = self.get_object()
        tasks = Task.objects.filter(block__project=instance)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(methods=['GET', 'POST'], detail=True)
    def blocks(self, request, pk):
        if request.method == 'GET':
            instance = self.get_object()
            blocks = Block.objects.filter(project=instance)
            serializer = BlockListSerializer(blocks, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            instance = self.get_object()
            serializer = BlockCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(project=instance)
                return Response(serializer.data)
            return Response(serializer.errors)


class ProjectRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'put', 'patch', 'delete']
    serializer_class = ProjectCreateSerializer
    queryset = Project.objects.all()

    def get_permissions(self):
        if self.request.method in ['put', 'patch', 'delete']:
            self.permission_classes = [IsOwner, ]
        else:
            self.permission_classes = [IsAuthenticated, ]
        return super(ProjectRetrieveUpdateDelete, self).get_permissions()


class BlockViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = Block.objects.all()
    permission_classes = (BlockPermission, )

    def get_serializer_class(self):
        if self.action == 'list':
            return BlockListSerializer
        if self.action == 'retrieve':
            return BlockDetailSerializer
        return BlockCreateSerializer

    @action(methods=['GET', 'POST'], detail=True)
    def tasks(self, request, pk):
        if request.method == 'GET':
            instance = self.get_object()
            tasks = Task.objects.filter(block=instance)
            serializer = TaskListSerializer(tasks, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            instance = self.get_object()
            serializer = TaskCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(block=instance, creator=request.user)
                return Response(serializer.data)
            return Response(serializer.errors)


class TaskViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (TaskPermission, )

    @action(methods=['GET'], detail=False)
    def my(self, request):
        tasks = Task.objects.filter(creator=self.request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(methods=['GET', 'POST'], detail=True)
    def comments(self, request, pk):
        if request.method == 'GET':
            instance = self.get_object()
            comments = TaskComment.objects.filter(task=instance)
            serializer = TaskCommentListSerializer(comments, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            instance = self.get_object()
            serializer = TaskCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(creator=request.user, task=instance)
                return Response(serializer.data)
            return Response(serializer.errors)

    @action(methods=['GET', 'POST'], detail=True)
    def documents(self, request, pk):
        if request.method == 'GET':
            instance = self.get_object()
            docs = TaskDocument.objects.filter(task=instance)
            serializer = TaskDocumentListSerializer(docs, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            instance = self.get_object()
            serializer = TaskDocumentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(creator=request.user, task=instance)
                return Response(serializer.data)
            return Response(serializer.errors)


class TaskCommentViewSet(mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = (TaskInsidePermission, )


class TaskDocumentViewSet(mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = TaskDocument.objects.all()
    serializer_class = TaskDocumentSerializer
    permission_classes = (TaskInsidePermission, )
