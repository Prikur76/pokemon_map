import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    current_time = localtime()
    pokemons = Pokemon.objects.filter(
        pokemonentity__appeared_at__lte=current_time,
        pokemonentity__disappeared_at__gt=current_time
    )
    pokemon_entities = PokemonEntity.objects.filter(
        pokemon__in=pokemons,
        appeared_at__lte=current_time,
        disappeared_at__gt=current_time
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            )
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append(
            {
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title_ru,
            }
        )
    return render(
        request,
        'mainpage.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemons': pokemons_on_page,
        }
    )


def show_pokemon(request, pokemon_id):
    pokemons = Pokemon.objects.filter(id=pokemon_id)
    pokemon_entities = PokemonEntity.objects.filter(pokemon_id=pokemon_id)

    for pokemon in pokemons:
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon
            break
        else:
            return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    return render(
        request, 'pokemon.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemon': requested_pokemon
        }
    )
