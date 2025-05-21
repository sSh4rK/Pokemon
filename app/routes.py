from flask import Blueprint, render_template
from .pokemon_service import PokemonService

main = Blueprint('main', __name__)

@main.route('/')
def index():
    pokemon_list = PokemonService.get_pokemon_list()
    return render_template('index.html', pokemons=pokemon_list['results'])

@main.route('/pokemon/<name>')
def pokemon_detail(name):
    pokemon = PokemonService.get_pokemon_detail(name)
    if pokemon:
        return render_template('pokemon_detail.html', pokemon=pokemon)
    return "Pokemon not found", 404 
