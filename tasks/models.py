from django.db import models
from accounts.models import SimpleUser


class Task(models.Model):
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'title'],
                name='unique_task_title_per_user'
            )
        ]

    def __str__(self):
        return f"{self.title} ({self.user.username})"

