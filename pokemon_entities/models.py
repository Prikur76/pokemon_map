from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(
        max_length=200,
        verbose_name='Название покемона (рус.)',
    )
    title_en = models.CharField(
        max_length=200,
        verbose_name='Название покемона (анг.)',
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name='Название покемона (яп.)',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True, null=True,
    )
    image = models.ImageField(
        upload_to='pokemons',
        verbose_name='Изображение',
        blank=True,
    )
    img_url = models.URLField(
        verbose_name='Ссылка на изображение',
        blank=True, null=True,
    )
    previous_evolution = models.ForeignKey(
        'self',
        verbose_name='Из кого эволюционировал',
        related_name='next_evolutions',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name_plural = 'Типы покемонов'
        ordering = ['title_ru']

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон',
        related_name='entities',
    )
    lat = models.FloatField(
        null=False, verbose_name='Широта',
    )
    lon = models.FloatField(
        null=False, verbose_name='Долгота',
    )
    appeared_at = models.DateTimeField(
        verbose_name='Создан',
    )
    disappeared_at = models.DateTimeField(
        verbose_name='Исчезает',
    )
    level = models.IntegerField(
        blank=True, null=True,
        verbose_name='Уровень',
    )
    health = models.IntegerField(
        blank=True, null=True,
        verbose_name='Здоровье',
    )
    strength = models.IntegerField(
        blank=True, null=True,
        verbose_name='Сила',
    )
    defence = models.IntegerField(
        blank=True, null=True,
        verbose_name='Защита',
    )
    stamina = models.IntegerField(
        blank=True, null=True,
        verbose_name='Выносливость',
    )

    class Meta:
        verbose_name_plural = 'Покемоны на карте'
        ordering = ['pokemon']

    def __str__(self):
        return self.pokemon.title_ru
