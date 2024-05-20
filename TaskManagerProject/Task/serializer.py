from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""
    class Meta:
        model = Task
        fields = '__all__'

class TaskUpdateSerializer(TaskSerializer):
    """Serializer for updating an existing Task"""
    class Meta:
        model = Task
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TaskUpdateSerializer, self).__init__(*args, **kwargs)
        # Make fields optional when updating
        for field_name, field in self.fields.items():
            field.required = False
