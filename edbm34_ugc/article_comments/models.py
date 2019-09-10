from django.db import models
from django_comments.abstracts import CommentAbstractModel


class ArticleComment(CommentAbstractModel):
    pass
    # title = models.CharField(max_length=300)
