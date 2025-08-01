# secret/models.py
from django.db import models
import uuid

class OneTimeSecret(models.Model):
    secret_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.secret_id)
