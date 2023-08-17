from django.db import models
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your models here.

class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return self.content
    
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']
        labels = {
            'title' : 'Заголовок',
            'content' : 'Содержание'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content' : 'Комментарий'
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'first_name',
            'last_name', 
            'password1', 
            'password2'
        ]