from django.urls import path
from . import views
from .views import NewsView, NewsDetailView, UpdateNewsView
app_name = 'news'
urlpatterns = [
    path('', NewsView.as_view(), name='news'),
    path('<int:news_id>/', NewsDetailView.as_view(),  name='news_detail'),
    path('<int:news_id>/edit/', UpdateNewsView.as_view(), name='news_edit')
]