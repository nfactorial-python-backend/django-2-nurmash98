from django.urls import path
from . import views
from .views import NewsView, NewsDetailView, UpdateNewsView
app_name = 'news'
urlpatterns = [

    path('', NewsView.as_view(), name='news'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('<int:news_id>/', NewsDetailView.as_view(),  name='news_detail'),
    path('<int:news_id>/edit/', UpdateNewsView.as_view(), name='news_edit'),
    path('<int:news_id>/delete/', views.delete_news, name='delete_news'),
    path('<int:news_id>/comment/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
]