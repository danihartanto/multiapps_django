from django.db import models
from django.contrib.auth.models import User

class MathGameScore(models.Model):
    LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='easy')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.score} pts ({self.level})"
