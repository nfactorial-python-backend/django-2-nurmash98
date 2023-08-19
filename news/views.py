from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import News, Comment, NewsForm, CommentForm, SignUpForm, User
from django.views import View
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from .serializers import NewsSerializer
from rest_framework import generics

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class NewsListCreateView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
class NewsDetailViewByGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

@api_view(['POST'])
def news_add(request):
    serializer = NewsSerializer(data=request.data)
    if serializer.is_valid():
        news = News(
            title = serializer.validated_data.get('title'),
            content = serializer.validated_data.get('content'),
            author = serializer.validated_data.get('author'),
        )
        news.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsView(View):
    def get(self, request):
        news = News.objects.all().order_by('-created_at')
        form = NewsForm()
        return render(request, 'news/index.html', {'list_news': news, 'form': form})
    
    @method_decorator(login_required(login_url='/login/'))
    @method_decorator(permission_required('news.add_news', login_url='/login/'))
    def post(self, request):
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return HttpResponseRedirect(request.path)
        return HttpResponseRedirect(request.path)
    

@login_required(login_url='/login/')
def delete_news(request, news_id):
    news_id = int(news_id)
    news = get_object_or_404(News, id=news_id)
    if request.user == news.author or request.user.has_perm("news.delete_news"):
        news.delete()
    return HttpResponseRedirect(reverse('news:news'))

class NewsDetailView(View):
    def get(self, request, news_id):
        news = get_object_or_404(News, id=news_id)
        form = CommentForm()
        comments = news.comments.all().order_by('-created_at')
        return render(request, 'news/detail.html', {'news': news, 'comments': comments, 'form': form})
    
    @method_decorator(login_required(login_url='/login/'))
    def post(self, request, news_id):
        news = get_object_or_404(News, id=news_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.news = news
            comment.save()
            return HttpResponseRedirect(request.path)
        return HttpResponseRedirect(request.path)

class UpdateNewsView(View):
    def get(self, request, news_id):
        news_id = int(news_id)
        news = get_object_or_404(News, id=news_id)
        form = NewsForm(instance=news)
        return render(request, 'news/update.html', {'news': news, 'form': form})
    
    @method_decorator(login_required(login_url='/login/'))
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
    
@login_required(login_url='/login/')
def delete_comment(request, news_id, comment_id):
    news_id = int(news_id)
    comment_id = int(comment_id)
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user or request.user.has_perm("news.delete_comment"):
        comment.delete()
    return HttpResponseRedirect(reverse('news:news_detail', args=[news_id]))

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid(): 
            user = form.save()
            group = Group.objects.get(name='default')
            group.user_set.add(user)
            login(request, user)
            return HttpResponseRedirect(reverse('news:news'))
    else:
        form = SignUpForm()
    return render(request, 'registration/sign-up.html', {'form': form})
    