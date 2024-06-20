from django.db import models

class Quiz(models.Model):
    quiz_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

class Participant(models.Model):
    username = models.CharField(max_length=100)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
