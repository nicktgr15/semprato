def get_model():
    from article_comments.models import ArticleComment
    return ArticleComment

def get_form():
    from article_comments.forms import ArticleCommentForm
    return ArticleCommentForm