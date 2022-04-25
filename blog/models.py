from django.db import models


class Post(models.Model):
    """Модель поста блога"""
    title = models.CharField(max_length=255, verbose_name="Название", db_index=True)
    slug = models.SlugField(max_length=255, verbose_name="URL", unique=True)
    content = models.TextField(verbose_name="Содержание", blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    def get_dict(self):
        """Метод получения словаря для json"""
        new_dict = {
            'id': self.pk,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'creation_date': self.creation_date.date(),
            'comments': [],
        }
        return new_dict

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Comment(models.Model):
    """Модель комментария блога"""
    post = models.ForeignKey('Post', on_delete=models.PROTECT, verbose_name="Пост")
    text = models.TextField(verbose_name="Текст")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    parent = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True, verbose_name="Родитель",
                               related_name="children")
    level = models.IntegerField(blank=True, null=True, verbose_name="Уровень вложенности")

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        """
        Данный метод переопределен для автоматического вычисления уровня вложенности
        А также дабы избежать возможности прикрепить вложенный комментарий, к посту,
        на который не ссылается родитель
        """
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

    def get_dict(self):
        """Метод получения словаря для json"""
        if self.parent:
            new_dict = {
                "id": self.pk,
                "level": self.level,
                "parent": self.parent.id,
                'post': self.post.id,
                'text': self.text,
                'creation_date': self.creation_date.date(),
                'child': [],
            }
        else:
            new_dict = {
                "id": self.pk,
                "level": self.level,
                "parent": None,
                'post': self.post.id,
                'text': self.text,
                'creation_date': self.creation_date.date(),
                'child': [],
            }
        return new_dict

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
