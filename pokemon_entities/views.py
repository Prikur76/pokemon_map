import folium
from django.shortcuts import render, get_object_or_404
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
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gt=current_time,
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons_on_page = []
    for pokemon_entity in pokemon_entities:
        pokemons_on_page.append(
            {
                'pokemon_id': pokemon_entity.pokemon.id,
                'img_url': request.build_absolute_uri(
                    pokemon_entity.pokemon.image.url
                ),
                'title_ru': pokemon_entity.pokemon.title_ru,
            }
        )
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(
                pokemon_entity.pokemon.image.url
            )
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
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    requested_pokemon = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'img_url': pokemon.image.url,
    }

    previous_evolution = pokemon.previous_evolution
    if previous_evolution:
        requested_pokemon.update(
            {
                'previous_evolution': {
                    'title_ru': previous_evolution.title_ru,
                    'pokemon_id': previous_evolution.id,
                    'img_url': previous_evolution.image.url,
                },
            }
        )

    next_evolution = pokemon.next_evolutions.first()
    if next_evolution:
        requested_pokemon.update(
            {
                'next_evolution': {
                    'title_ru': next_evolution.title_ru,
                    'pokemon_id': next_evolution.id,
                    'img_url': next_evolution.image.url,
                },
            }
        )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(
        pokemon_id=pokemon_id
    )
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(
                pokemon_entity.pokemon.image.url
            )
        )
    return render(
        request,
        'pokemon.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemon': requested_pokemon
        }
    )
