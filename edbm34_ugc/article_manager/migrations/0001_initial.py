# Generated by Django 2.1.5 on 2019-05-27 16:37

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import location_field.models.plain
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', ckeditor_uploader.fields.RichTextUploadingField()),
                ('title', models.CharField(max_length=100)),
                ('enable_comments', models.BooleanField(default=True)),
                ('contains_blocked_terms', models.BooleanField(default=False)),
                ('irregular_image_date', models.BooleanField(default=False)),
                ('publish', models.BooleanField(default=False)),
                ('image1', models.ImageField(blank=True, default=None, null=True, upload_to='images')),
                ('image1_exif_datetime', models.DateTimeField(blank=True, default=None, null=True)),
                ('image1_location', location_field.models.plain.PlainLocationField(blank=True, max_length=63, null=True)),
                ('image2', models.ImageField(blank=True, default=None, null=True, upload_to='images')),
                ('image2_exif_datetime', models.DateTimeField(blank=True, default=None, null=True)),
                ('image2_location', location_field.models.plain.PlainLocationField(blank=True, max_length=63, null=True)),
                ('image3', models.ImageField(blank=True, default=None, null=True, upload_to='images')),
                ('image3_exif_datetime', models.DateTimeField(blank=True, default=None, null=True)),
                ('image3_location', location_field.models.plain.PlainLocationField(blank=True, max_length=63, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='article_author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BlockedTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=40)),
                ('name', models.CharField(max_length=100)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='article_manager.Category')),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='article_category', to='article_manager.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='inferred_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inferred_article_category', to='article_manager.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='article_manager.ArticleTag'),
        ),
    ]
