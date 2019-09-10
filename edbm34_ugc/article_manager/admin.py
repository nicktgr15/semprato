from django.contrib import admin
from django.contrib.admin import StackedInline, ModelAdmin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin

from article_manager.models import Category, Article, BlockedTerm, ArticleTag


class ArticleInline(StackedInline):
    model = Article
    extra = 0
    fk_name = 'category'


class CategoryAdmin(MPTTModelAdmin):
    inlines = [ArticleInline]


API_KEY = "AIzaSyCnyIBkxzS_ZiqhH304f8BQO1fzgakzaxY"


class ArticleAdmin(ModelAdmin):
    list_filter = ['category']
    list_display = ('title', 'publish', 'enable_comments', 'contains_blocked_terms', 'irregular_image_date', 'author')

    fieldsets = (
        (None, {
            'fields': ('created_at', 'title', 'text', 'likes', 'tags', 'author', 'category', 'inferred_category',
                       'enable_comments', 'contains_blocked_terms', 'irregular_image_date', 'publish')
        }),
        ('Image 1', {
            'fields': ('image1', 'image1_map_location', 'image1_thumb', 'image1_exif_datetime',),
        }),
        ('Image 2', {
            'fields': ('image2', 'image2_map_location', 'image2_thumb', 'image2_exif_datetime',),
        }),
        ('Image 3', {
            'fields': ('image3', 'image3_map_location', 'image3_thumb', 'image3_exif_datetime',),
        })
    )

    readonly_fields = ('created_at', 'image1_thumb', 'image2_thumb', 'image3_thumb', 'image1_map_location',
                       'image2_map_location', 'image3_map_location',
                       'image1_exif_datetime', 'image2_exif_datetime', 'image3_exif_datetime',)

    def image1_map_location(self, obj):
        if obj.image1_location is not None and obj.image1_location != '':
            html = '<img src="https://maps.googleapis.com/maps/api/staticmap?' \
                   '&zoom=7' \
                   '&size=200x200' \
                   '&maptype=roadmap ' \
                   '&markers=color:blue%7Clabel:S%7C{location}' \
                   '&key={api_key}" title="" />'
            return format_html(html.format(location=obj.image1_location, api_key=API_KEY))
        else:
            return "-"

    def image2_map_location(self, obj):
        if obj.image2_location is not None and obj.image2_location != '':
            html = '<img src="https://maps.googleapis.com/maps/api/staticmap?' \
                   '&zoom=7' \
                   '&size=200x200' \
                   '&maptype=roadmap ' \
                   '&markers=color:blue%7Clabel:S%7C{location}' \
                   '&key={api_key}" title="" />'
            return format_html(html.format(location=obj.image2_location, api_key=API_KEY))
        else:
            return "-"

    def image3_map_location(self, obj):
        if obj.image3_location is not None and obj.image3_location != '':
            html = '<img src="https://maps.googleapis.com/maps/api/staticmap?' \
                   '&zoom=7' \
                   '&size=200x200' \
                   '&maptype=roadmap ' \
                   '&markers=color:blue%7Clabel:S%7C{location}' \
                   '&key={api_key}" title="" />'
            return format_html(html.format(location=obj.image3_location, api_key=API_KEY))
        else:
            return "-"

    def image1_thumb(self, obj):
        html = '<a href="{url}" target="_blank"><img width=150 src="{url}" /></a>'
        return format_html(html.format(url=obj.image1.url))

    def image2_thumb(self, obj):
        html = '<a href="{url}" target="_blank"><img width=150 src="{url}" /></a>'
        return format_html(html.format(url=obj.image2.url))

    def image3_thumb(self, obj):
        html = '<a href="{url}" target="_blank"><img width=150 src="{url}" /></a>'
        return format_html(html.format(url=obj.image3.url))


class ArticleTagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleTag, ArticleTagAdmin)


class BlockedTermAdmin(admin.ModelAdmin):
    pass


admin.site.register(BlockedTerm, BlockedTermAdmin)
