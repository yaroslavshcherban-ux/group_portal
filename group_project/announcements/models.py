from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_date = models.DateField(null=True, blank=True)
    is_pinned = models.BooleanField(default=False)

    file = models.FileField(upload_to='announcements/', blank=True, null=True)
    image = models.ImageField(upload_to='announcements/images/', blank=True, null=True, verbose_name='Зображення')

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likes.count()


# Система лайків
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'announcement')
    def __str__(self):
        return f"{self.user} лайкнув {self.announcement}" 

class Comment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Коментар від {self.author} до {self.announcement}'
