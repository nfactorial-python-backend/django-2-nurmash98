# Generated by Django 4.2.4 on 2023-08-10 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_comment_news_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='news_id',
            new_name='news',
        ),
    ]
