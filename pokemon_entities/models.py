from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pokemons', blank=True, null=True)

    def __str__(self):
        return self.title    # noqa F405


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    latitude = models.FloatField(verbose_name='Lat.', null=False)
    longitude = models.FloatField(verbose_name='Lon.', null=False)
    appeared_at = models.DateTimeField(verbose_name='Appeared at', blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name='Disappeared at', blank=True, null=True)
    level = models.IntegerField(verbose_name='Level', blank=True, null=True)
    helth = models.IntegerField(verbose_name='Health', blank=True, null=True)
    strength = models.IntegerField(verbose_name='Strength', blank=True, null=True)
    defence = models.IntegerField(verbose_name='Defence', blank=True, null=True)
    stamina = models.IntegerField(verbose_name='Stamina', blank=True, null=True)

    def __str__(self):
        return self.latitude, self.longitude