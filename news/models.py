from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def has_comments(self):
        comment = Comment.objects.filter(news=self)
        if comment:
            return True
        else:
            return False
    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.content