from django.db import models


class Category(models.Model):
    name = models.CharField(
        'Категория',
        max_length=150,
        unique=True
    )
    slug = models.SlugField(
        'Cлаг',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        'Жанр',
        max_length=100
    )
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=200)
    year = models.IntegerField('Дата выпуска')
    description = models.TextField('Описание')
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        related_name='genre',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
