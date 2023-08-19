from django.urls import path
from . import views
from .views import NewsView, NewsDetailView, UpdateNewsView, NewsListCreateView, NewsDetailViewByGenerics
app_name = 'news'
urlpatterns = [

    path('', views.NewsView.as_view(),  name='news'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('<int:news_id>/', NewsDetailView.as_view(),  name='news_detail'),
    path('<int:news_id>/edit/', UpdateNewsView.as_view(), name='news_edit'),
    path('<int:news_id>/delete/', views.delete_news, name='delete_news'),
    path('<int:news_id>/comment/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
    path('api/news/', NewsListCreateView.as_view(), name='api_news'),
    path('api/news/<int:pk>/', NewsDetailViewByGenerics.as_view(), name='news-detail')
]