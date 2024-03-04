from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('authors')
        ordering = ["name"]

    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField(null=True, blank=True)

    @property
    def bio_short(self) -> str:
        if len(self.bio) < 48:
            return self.bio
        return self.bio[:48] + "..."


class Category(models.Model):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('categories')
        ordering = ["name"]

    name = models.CharField(max_length=40, db_index=True)


class Tag(models.Model):
    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('tags')
        ordering = ["name"]

    name = models.CharField(max_length=20, db_index=True)


class Article(models.Model):
    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('articles')
        ordering = ["pub_date"]

    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField(null=True, blank=True, db_index=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="articles")

    @property
    def content_short(self) -> str:
        if len(self.content) < 48:
            return self.content
        return self.content[:48] + "..."