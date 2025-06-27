from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task
from tasks.serialazers.serialazer import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['patch'], url_path='update')
    def update_by_title(self, request):
        original_title = request.data.get('original_title')
        new_title = request.data.get('title')  # title mới

        if not original_title:
            return Response({"detail": "Missing 'original_title'."}, status=400)

        try:
            task = Task.objects.get(user=request.user, title=original_title)
        except Task.DoesNotExist:
            return Response({"detail": f"Task with title '{original_title}' not found."}, status=404)


        if new_title and new_title != original_title:
            if Task.objects.filter(user=request.user, title=new_title).exclude(id=task.id).exists():
                return Response(
                    {"detail": f"Title '{new_title}' already exists for this user."},
                    status=400
                )
        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)

    @action(detail=False, methods=['delete'], url_path='delete')
    def delete_by_title(self, request):
        title = request.query_params.get('title')
        if not title:
            return Response({"detail": "Missing title."}, status=400)

        try:
            task = Task.objects.get(user=request.user, title=title)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found."}, status=404)

        task.delete()
        return Response({"detail": "Deleted successfully."},status=200)
