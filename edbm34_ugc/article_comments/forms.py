from django_comments.forms import CommentForm


class ArticleCommentForm(CommentForm):
    # title = forms.CharField(max_length=300)

    def get_comment_create_data(self, **kwargs):
        # Use the data of the superclass, and add in the title field
        data = super(ArticleCommentForm, self).get_comment_create_data()
        # data['title'] = self.cleaned_data['title']
        return data