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
        if pokemon not in pokemons_on_page:
            pokemons_on_page.append(
                {
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.image.url),
                'title_ru': pokemon.title_ru,
                }
            )
    pokemons_without_duplicates = map(
        dict,
        set(tuple(sorted(pokemon.items())) for pokemon in pokemons_on_page)
    )
    return render(
        request,
        'mainpage.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemons': pokemons_without_duplicates,
        }
    )


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    pokemon_entities = PokemonEntity.objects.filter(pokemon_id=pokemon_id)
    if pokemon.id == int(pokemon_id):
        previous_evolution = pokemon.previous_evolution
        next_evolution = pokemon.previous_evolutions.all().first()
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    requested_pokemon = {}
    requested_pokemon['pokemon_id'] = pokemon.id
    requested_pokemon['title_ru'] = pokemon.title_ru
    requested_pokemon['title_en'] = pokemon.title_en
    requested_pokemon['title_jp'] = pokemon.title_jp
    requested_pokemon['description'] = pokemon.description
    requested_pokemon['img_url'] = pokemon.image.url
    if previous_evolution:
        requested_pokemon['previous_evolution'] = {
            'title_ru': previous_evolution.title_ru,
            'pokemon_id': previous_evolution.id,
            'img_url': previous_evolution.image.url
        }
    if next_evolution:
        requested_pokemon['next_evolution'] = {
            'title_ru': next_evolution.title_ru,
            'pokemon_id': next_evolution.id,
            'img_url': next_evolution.image.url
        }
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    return render(
        request,
        'pokemon.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemon': requested_pokemon
        }
    )
