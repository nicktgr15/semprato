from django import forms

from article_manager.models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['category', 'text', 'title', 'image1', 'image2', 'image3']
