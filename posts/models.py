from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile


class Post(models.Model):
    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = 'Посты'
        ordering = ('-created',)

    content = models.TextField(verbose_name="Пост")
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])],
                              blank=True, verbose_name="Изображение")
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes', verbose_name="Лайкнул")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts", verbose_name="Автор")

    def __str__(self):
        return str(self.content[:20])

    def num_likes(self):
        return self.liked.all().count()

    # num of comments here
    def num_comments(self):
        return self.comment_set.all().count()


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Пользователь")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    body = models.TextField(max_length=300, verbose_name="Текст")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = 'Коментарии'


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Пользователь")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    value = models.CharField(max_length=10, choices=LIKE_CHOICES, verbose_name="Значение")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = 'Лайки'
