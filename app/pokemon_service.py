import requests

class PokemonService:
    BASE_URL = "https://pokeapi.co/api/v2"
    
    @staticmethod
    def get_pokemon_list(limit=151):
        response = requests.get(f"{PokemonService.BASE_URL}/pokemon?limit={limit}")
        return response.json()

    @staticmethod
    def get_pokemon_detail(pokemon_name):
        try:
            response = requests.get(f"{PokemonService.BASE_URL}/pokemon/{pokemon_name.lower()}")
            pokemon_data = response.json()
            
            # Récupération des informations sur l'espèce
            species_response = requests.get(pokemon_data['species']['url'])
            species_data = species_response.json()
            
            # Récupération de la description en français
            description = next(
                (entry['flavor_text'] for entry in species_data['flavor_text_entries'] 
                 if entry['language']['name'] == 'fr'),
                "Description non disponible"
            )
            
            return {
                'id': pokemon_data['id'],
                'name': pokemon_data['name'],
                'image': pokemon_data['sprites']['other']['official-artwork']['front_default'],
                'types': [t['type']['name'] for t in pokemon_data['types']],
                'height': pokemon_data['height'] / 10,
                'weight': pokemon_data['weight'] / 10,
                'stats': {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']},
                'cry_url': f"https://play.pokemonshowdown.com/audio/cries/{pokemon_data['name']}.mp3",
                'description': description
            }
        except Exception as e:
            print(f"Error fetching pokemon: {e}")
            return None 