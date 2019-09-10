from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from mptt.managers import TreeManager
from django.contrib.auth.models import User
from django_comments.moderation import CommentModerator, moderator
from location_field.models.plain import PlainLocationField


class CategoryManager(TreeManager):
    pass


class Category(MPTTModel):

    objects = CategoryManager()

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.PROTECT)
    slug = models.SlugField(max_length=40)
    name = models.CharField(max_length=100)

    # class MPTTMeta:
    #     order_insertion_by = ['title']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class ArticleTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True)
    tags = models.ManyToManyField(ArticleTag, blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='article_author', blank=True, null=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 related_name='article_category')
    inferred_category = models.ForeignKey(Category,
                                          on_delete=models.PROTECT, related_name='inferred_article_category')
    text = RichTextUploadingField()
    title = models.CharField(max_length=100)
    enable_comments = models.BooleanField(default=True)
    contains_blocked_terms = models.BooleanField(default=False)
    irregular_image_date = models.BooleanField(default=False)

    publish = models.BooleanField(default=False)

    image1 = models.ImageField(upload_to="images", default=None, blank=True, null=True)
    image1_exif_datetime = models.DateTimeField(default=None, blank=True, null=True)
    image1_location = PlainLocationField(based_fields=['city'], zoom=3, blank=True, null=True)

    image2 = models.ImageField(upload_to="images", default=None, blank=True, null=True)
    image2_exif_datetime = models.DateTimeField(default=None, blank=True, null=True)
    image2_location = PlainLocationField(based_fields=['city'], zoom=3, blank=True, null=True)

    image3 = models.ImageField(upload_to="images", default=None, blank=True, null=True)
    image3_exif_datetime = models.DateTimeField(default=None, blank=True, null=True)
    image3_location = PlainLocationField(based_fields=['city'], zoom=3, blank=True, null=True)

    def __str__(self):
        return self.title


class ArticleModerator(CommentModerator):
    enable_field = 'enable_comments'

    def moderate(self, comment, content_object, request):
        terms = [term.name for term in BlockedTerm.objects.all()]
        for term in terms:
            if term in comment.comment:
                return True

        return False


moderator.register(Article, ArticleModerator)


class BlockedTerm(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

