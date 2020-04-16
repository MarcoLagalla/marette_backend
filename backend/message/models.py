from django.db import models


class Message(models.Model):
    email = models.CharField(default='prova@email.com', max_length=200)
    subject = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.subject

