from django.db import models

class ChatRule(models.Model):
    keyword = models.CharField(max_length=255)
    response = models.TextField()

    def __str__(self):
        return self.keyword
