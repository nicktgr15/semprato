# Generated by Django 2.1.5 on 2019-05-27 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article_comments', '0002_auto_20190527_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentwithtitle',
            name='title',
        ),
    ]
