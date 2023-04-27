from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pokemons', blank=True, null=True)

    def __str__(self):
        return self.title    # noqa F405


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    latitude = models.FloatField(verbose_name='Lat.')
    longitude = models.FloatField(verbose_name='Lon.')


    def __str__(self):
        return self.latitude, self.longitude