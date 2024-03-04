from django.shortcuts import render
from django.views.generic import ListView
from blogapp.models import Article


# Create your views here.
class ArticleListView(ListView):
    template_name = "blogapp/articles_list.html"
    context_object_name = "articles"
    queryset = Article.objects.select_related("author").prefetch_related("tags").defer("content", "author__bio")
