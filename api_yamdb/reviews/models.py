from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

USER_ROLES = (
    ('MODERATOR', 'Модератор'),
    ('ADMINISTRATOR', 'Администратор'),
    ('USER', 'Авторизованный пользователь'),
)


class User(AbstractUser):

    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=50,
        default='USER',
        choices=USER_ROLES
    )

    def __str__(self):
        return self.username

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user')
        ]


class Title(models.Model):
    ...


class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField('Текст', help_text='Отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.SmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        # default=0
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'],
                name='unique_review'
            )
        ]


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField('Текст', help_text='Комментарий')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
