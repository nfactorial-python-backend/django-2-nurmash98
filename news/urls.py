from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:news_id>/', views.get_news, name='get_news'),
    path('/add_news', views.add_news, name='add_news'),
]