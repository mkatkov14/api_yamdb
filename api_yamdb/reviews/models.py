from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.CharField(
        max_length=50,
        verbose_name="Роль",
        default="user"
    )


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Категория",
        help_text="Проверьте название категории",
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Жанр",
        help_text="Проверьте название жанра",
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Произведение",
        help_text="Проверьте название произведения",
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска", help_text="Проверьте название год выпуска"
    )
    description = models.TextField(verbose_name="Описание произведения")
    genre = models.ManyToManyField(
        Genre,
        through='genre_title',
<<<<<<< HEAD

        related_name="titles",
        blank=True,

=======
        # on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        # null=True,
>>>>>>> master
        verbose_name="Жанр произведения",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
        verbose_name="Категория произведения",
    )

    class Meta:
        ordering = ["-year"]

    def __str__(self):
        return self.name


class genre_title(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField("Текст", help_text="Отзыв")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.SmallIntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        # default=0
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["title_id", "author"], name="unique_review"
            )
        ]


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField("Текст", help_text="Комментарий")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-pub_date"]
