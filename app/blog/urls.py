from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.BlogListView.as_view(), name = 'blog'),
    path('article/<int:pk>/<str:title>', views.ArticleListView.as_view(), name = 'article'),
    path('nese', TemplateView.as_view(template_name = 'example.html'))
]