from django.contrib import admin

# Register your models here.

from .models import News, Comment

# admin.site.register(News)
# admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 5


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'has_comments')
    inlines = [CommentInline]
    
admin.site.register(News, NewsAdmin)