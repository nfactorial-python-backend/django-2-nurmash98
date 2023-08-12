from django.test import TestCase
from django.utils import timezone
from .models import News, Comment

from django.urls import reverse

# Create your tests here.
class NewsTests(TestCase):
    def test_has_comments_true(self):
        news = News(title="Test Title", content = "Test Content")
        news.save()
        comment = Comment(content = "Test Comment", news = news)
        comment.save()
        self.assertTrue(news.has_comments())

    def test_has_comments_false(self):
        news = News(title="Test Title 1", content = "Test Content 1")
        news.save()
        self.assertFalse(news.has_comments())
    
    def test_news_order(self):
        news1 = News.objects.create(title='News 1', content='Content 1')
        news1.save()
        news2 = News.objects.create(title='News 2', content='Content 2')
        news2.save()
        response = self.client.get(reverse('news:index'))
        news_list = list(response.context['list_news'])
        self.assertEqual(news_list, [news2, news1])

    def test_news_detail(self):
        news = News.objects.create(title='News 1', content='Content 1')
        news.save()
        response = self.client.get(reverse('news:get_news', args=[news.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['news'].title, news.title)
        self.assertEqual(response.context['news'].content, news.content)

    def test_news_comments_order(self):
        news = News.objects.create(title='News 1', content='Content 1')
        comment1 = Comment.objects.create(content='Comment 1', news=news)
        comment1.save()
        comment2 = Comment.objects.create(content='Comment 2', news=news)
        comment2.save()
        response = self.client.get(reverse('news:get_news', args=[news.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['comments']), [comment2, comment1])
                                        




