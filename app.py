from app import create_app
import requests

app = create_app()

def get_pokemon(name):
    try:
        # Récupérer les données de base du Pokémon
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name.lower()}')
        if response.status_code == 200:
            data = response.json()
            
            # Récupérer la description en français
            species_response = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{data["id"]}')
            species_data = species_response.json()
            description = next(
                (entry['flavor_text'] for entry in species_data['flavor_text_entries'] 
                 if entry['language']['name'] == 'fr'),
                "Description non disponible"
            )

            pokemon = {
                'id': data['id'],
                'name': data['name'],
                'image': data['sprites']['other']['official-artwork']['front_default'],
                'types': [t['type']['name'] for t in data['types']],
                'height': data['height'] / 10,  # Conversion en mètres
                'weight': data['weight'] / 10,  # Conversion en kg
                'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
                'cry_url': f"https://play.pokemonshowdown.com/audio/cries/{data['name']}.mp3",
                'description': description
            }
            return pokemon
    except Exception as e:
        print(f"Erreur lors de la récupération du Pokémon: {e}")
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 
