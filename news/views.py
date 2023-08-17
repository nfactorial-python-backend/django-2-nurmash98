from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import News, Comment, NewsForm, CommentForm
from django.views import View
from django.urls import reverse


class NewsView(View):
    def get(self, request):
        news = News.objects.all().order_by('-created_at')
        form = NewsForm()
        return render(request, 'news/index.html', {'list_news': news, 'form': form})
    
    def post(self, request):
        form = NewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            news = News(title=title, content=content)
            news.save()
            return HttpResponseRedirect(request.path)
        return HttpResponseRedirect(request.path)

class NewsDetailView(View):
    def get(self, request, news_id):
        news = get_object_or_404(News, id=news_id)
        form = CommentForm()
        comments = news.comments.all().order_by('-created_at')
        return render(request, 'news/detail.html', {'news': news, 'comments': comments, 'form': form})
    
  
    def post(self, request, news_id):
        news = get_object_or_404(News, id=news_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            comment = Comment(content=content, news=news)
            comment.save()
            return HttpResponseRedirect(request.path)
        return HttpResponseRedirect(request.path)

class UpdateNewsView(View):
    def get(self, request, news_id):
        news_id = int(news_id)
        news = get_object_or_404(News, id=news_id)
        form = NewsForm(instance=news)
        return render(request, 'news/update.html', {'news': news, 'form': form})
    
    def post(self, request, news_id):
        news_id = int(news_id)
        news = get_object_or_404(News, id=news_id)
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            news.title = title
            news.content = content
            news.save()
            return HttpResponseRedirect(reverse('news:news_detail', args=[news.id]))
        return HttpResponseRedirect(request.path)
    