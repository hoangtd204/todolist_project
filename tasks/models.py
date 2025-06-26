from django.db import models
from accounts.models import SimpleUser

class Task(models.Model):
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
