from django.contrib import admin

# Register your models here.
from django.contrib.admin.options import ModelAdmin
from article_comments.models import ArticleComment


class CommentAdmin(ModelAdmin):

    list_display = ('name', 'get_article_title', 'get_article_author', 'submit_date', 'is_public', 'is_removed')
    list_filter = ('submit_date', 'site', 'is_public', 'is_removed')
    date_hierarchy = 'submit_date'
    ordering = ('-submit_date',)

    def get_article_title(self, obj):
        return obj.content_object
    get_article_title.short_description = 'Article Title'

    def get_article_author(self, obj):
        return obj.content_object.author
    get_article_author.short_description = 'Article Author'


admin.site.register(ArticleComment, CommentAdmin)
