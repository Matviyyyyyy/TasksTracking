from django.db import models
from django.contrib.auth.models import User
from datetime import date
from auth_system.models import CustomUser
class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "To do"),
        ("in_progress", "In Progres"),
        ("done", "Done")
    ]
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High")
    ]

    name = models.CharField(max_length=256)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="todo")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["name"]

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to="comments_media/", blank=True, null=True)

    def __str__(self):
        return f"{self.published_date}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-published_date"]

class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')  # Забезпечує унікальність лайків

class Subscribe(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscribes')
    subscriber = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="subscribes_to")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('subscriber', 'user')