from django.db import models
from django.utils import timezone


class Pokemon(models.Model):
    title_ru = models.CharField(
        max_length=200,
        verbose_name='Название покемона (рус.)',
        default='Покемон',
    )
    title_en = models.CharField(
        max_length=200,
        verbose_name='Название покемона (анг.)',
        default='Pokemon',
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name='Название покемона (яп.)',
        default='ポケモン',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True, null=True,
        default='существо Вселенной Покемон Гоу'
    )
    image = models.ImageField(
        upload_to='pokemons',
        verbose_name='Изображение',
        blank=True,
        default='pokemons/default.png'
    )
    img_url = models.URLField(
        verbose_name='Ссылка на изображение',
        blank=True, null=True,
    )
    previous_evolution = models.ForeignKey(
        'self',
        verbose_name='Из кого эволюционировал',
        related_name='previous_evolutions',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон',
    )
    lat = models.FloatField(
        null=False, verbose_name='Широта',
    )
    lon = models.FloatField(
        null=False, verbose_name='Долгота',
    )
    appeared_at = models.DateTimeField(
        verbose_name='Создан',
        default=timezone.now
    )
    disappeared_at = models.DateTimeField(
        verbose_name='Исчезает',
        default=timezone.now
    )
    level = models.IntegerField(
        blank=True,
        verbose_name='Уровень',
        default=0
    )
    health = models.IntegerField(
        blank=True,
        verbose_name='Здоровье',
        default=0
    )
    strength = models.IntegerField(
        blank=True,
        verbose_name='Сила',
        default=0
    )
    defence = models.IntegerField(
        blank=True,
        verbose_name='Защита',
        default=0
    )
    stamina = models.IntegerField(
        blank=True,
        verbose_name='Выносливость',
        default=0
    )

    def __str__(self):
        return self.pokemon.title_ru