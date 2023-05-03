from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(
        max_length=200, default='Покемон'
    )
    title_en = models.CharField(
        max_length=200, default='Pokemon'
    )
    title_jp = models.CharField(
        max_length=200, default='ポケモン'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True, null=True
    )
    image = models.ImageField(
        upload_to='media/pokemons',
        blank=True, null=True
    )
    img_url = models.URLField(
        blank=True, null=True
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE
    )
    lat = models.FloatField(
        null=False, verbose_name='Lat.',
    )
    lon = models.FloatField(
        null=False, verbose_name='Lon.',
    )
    appeared_at = models.DateTimeField(
        blank=True, null=True,
        verbose_name='Appeared at',
    )
    disappeared_at = models.DateTimeField(
        blank=True, null=True,
        verbose_name='Disappeared at',
    )
    level = models.IntegerField(
        blank=True, null=True,
        verbose_name='Level',
    )
    helth = models.IntegerField(
        blank=True, null=True,
        verbose_name='Health',
    )
    strength = models.IntegerField(
        blank=True, null=True,
        verbose_name='Strength',
    )
    defence = models.IntegerField(
        blank=True, null=True,
        verbose_name='Defence',
    )
    stamina = models.IntegerField(
        blank=True, null=True,
        verbose_name='Stamina',
    )
    next_evolutions = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='next_evolutions',
        blank=True, null=True
    )
    previous_evolutions = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='previous_evolutions',
        blank=True, null=True
    )

    def __str__(self):
        return self.pokemon.title_ru