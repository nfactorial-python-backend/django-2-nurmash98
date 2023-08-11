from django.shortcuts import render, redirect, get_object_or_404
from .models import News



def index(request):
    news = News.objects.all().order_by('-created_at')
    return render(request, 'news/index.html', {'list_news': news})

def get_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    return render(request, 'news/detail.html', {'news': news})

def add_news(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        news = News(title=title, content=content)
        news.save()
        return redirect('news:index')
    return render(request, 'news:index')    
    