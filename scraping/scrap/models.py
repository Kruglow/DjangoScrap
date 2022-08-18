from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название города')
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = 'Название города'
        verbose_name_plural = 'Название городов'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='Язык програмирования')
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = 'Название языка'
        verbose_name_plural = 'Название языков'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(verbose_name='Название вакансии', max_length=250)
    company = models.CharField(verbose_name='Название компании', max_length=250)
    description = models.TextField(verbose_name='Описание')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='Язык програмирования')
    date = models.DateTimeField(verbose_name='Дата размещения', auto_now_add=True)

    class Meta:
        verbose_name = 'Название вакансии'
        verbose_name_plural = 'Название вакансий'

    def __str__(self):
        return self.title

