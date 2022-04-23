from django.db import models


class Post(models.Model):
    """Модель поста блога"""
    title = models.CharField(max_length=255, verbose_name="Название", db_index=True)
    slug = models.SlugField(max_length=255, verbose_name="URL", unique=True)
    content = models.TextField(verbose_name="Содержание", blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.PROTECT, verbose_name="Пост")
    text = models.TextField(verbose_name="Текст")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    parent = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True, verbose_name="Родитель",
                               related_name="children")
    level = models.IntegerField(blank=True, null=True, verbose_name="Уровень вложенности")

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.parent is None:
            self.level = 1
        else:
            parent = Comment.objects.get(pk=int(self.parent.pk))
            if self.post != parent.post:
                self.post = parent.post
            if self.parent is None:
                self.level = 1
            else:
                self.level = parent.level + 1
        super(Comment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
