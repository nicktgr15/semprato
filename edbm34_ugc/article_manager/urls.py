from article_manager import views
from django.urls import path

app_name = 'article_manager'


urlpatterns = [
    path('<category_name>/<article_id>/', views.article, name='article'),
    path('home/', views.home, name='home'),
    path('post_article/', views.post_article, name='post_article'),
    path('<category_slug>/<article_id>/like', views.post_like_article, name='post_like_article'),
    # path('post_article_step_2/', views.post_article_step_2, name='post_article_step_2'),
    path('<category_name>/', views.category, name='category'),
    path('', views.category, name='category'),
]
