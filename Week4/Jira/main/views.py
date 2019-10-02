from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from main.serializers import ProjectSerializer, BlockSerializer, TaskSerializer, TaskCommentSerializer, \
    TaskDocumentSerializer, ProjectDetailedSerializer
from main.models import Project, Block, Task, TaskComment, TaskDocument
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from main.permissions import IsOwner, BlockPermission, TaskPermission, TaskInsidePermission
from django.shortcuts import get_object_or_404


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


class ProjectViewSet(mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    http_method_names = ['get', 'post']
    queryset = Project.objects.all()
    # serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailedSerializer
        return ProjectSerializer

    # def retrieve(self, request, pk=None):
    #     queryset = Project.objects.all()
    #     project = get_object_or_404(queryset, pk=pk)
    #     serializer = ProjectDetailedSerializer(project)
    #     return Response(serializer.data)

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
            serializer = TaskSerializer(blocks, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            instance = self.get_object()
            request.data['project'] = instance.id
            serializer = BlockSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)


class ProjectRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'put', 'patch', 'delete']
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_permissions(self):
        if self.request.method in ['put', 'patch', 'delete']:
            self.permission_classes = [IsOwner, ]
        else:
            self.permission_classes = [IsAuthenticated, ]
        return super(ProjectRetrieveUpdateDelete, self).get_permissions()


class BlockViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    permission_classes = (BlockPermission, )

    @action(methods=['GET', 'POST'], detail=True)
    def tasks(self, request, pk):
        if request.method == 'GET':
            instance = self.get_object()
            tasks = Task.objects.filter(block=instance)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            instance = self.get_object()
            request.data['block'] = instance.id
            request.data['creator'] = request.user.id
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)


class TaskViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (TaskPermission, )

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)

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
            serializer = TaskCommentSerializer(comments, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            instance = self.get_object()
            request.data['creator'] = request.user.id
            request.data['task'] = instance.id
            serializer = TaskCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)

    @action(methods=['GET', 'POST'], detail=True)
    def documents(self, request, pk):
        if request.method == 'GET':
            instance = self.get_object()
            docs = TaskDocument.objects.filter(task=instance)
            serializer = TaskDocumentSerializer(docs, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            instance = self.get_object()
            request.data['creator'] = request.user.id
            request.data['task'] = instance.id
            serializer = TaskDocumentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)


class TaskCommentViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = (TaskInsidePermission, )

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)


class TaskDocumentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = TaskDocument.objects.all()
    serializer_class = TaskDocumentSerializer
    permission_classes = (TaskInsidePermission, )

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)
