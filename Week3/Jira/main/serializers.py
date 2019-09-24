from main.models import Project, Block, Task, TaskComment, TaskDocument
from rest_framework import serializers
from authe.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'

class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'

class TaskDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'