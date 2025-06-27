from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'completed', 'created_at', 'username']
        read_only_fields = ['id', 'created_at', 'username']

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        title = attrs.get('title')

        if self.instance:
            #For update
            if self.instance.title == title:
                return attrs
            if Task.objects.filter(user=user, title=title).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError({"title": "You already have a task with this title."})
        else:
            # For creation
            if Task.objects.filter(user=user, title=title).exists():
                raise serializers.ValidationError({"title": "You already have a task with this title."})

        return attrs


