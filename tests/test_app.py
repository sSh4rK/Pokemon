import pytest
from app import create_app
from unittest.mock import patch

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# Mock data pour les tests
MOCK_POKEMON_LIST = {
    "results": [
        {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
        {"name": "charmander", "url": "https://pokeapi.co/api/v2/pokemon/4/"}
    ]
}

MOCK_POKEMON_DETAIL = {
    "id": 1,
    "name": "bulbasaur",
    "sprites": {
        "other": {
            "official-artwork": {
                "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png"
            }
        }
    },
    "types": [{"type": {"name": "grass"}}, {"type": {"name": "poison"}}],
    "height": 7,
    "weight": 69,
    "stats": [
        {"base_stat": 45, "stat": {"name": "hp"}},
        {"base_stat": 49, "stat": {"name": "attack"}}
    ],
    "species": {"url": "https://pokeapi.co/api/v2/pokemon-species/1/"}
}

MOCK_SPECIES_DATA = {
    "flavor_text_entries": [
        {
            "flavor_text": "Un Pokémon très spécial.",
            "language": {"name": "fr"}
        }
    ]
}

def test_index_route(client):
    """Test de la route principale"""
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_POKEMON_LIST
        
        response = client.get('/')
        assert response.status_code == 200
        assert b'bulbasaur' in response.data
        assert b'charmander' in response.data

def test_pokemon_detail_route(client):
    """Test de la route de détail d'un Pokémon"""
    with patch('requests.get') as mock_get:
        # Configuration des retours pour les différents appels API
        def mock_get_side_effect(url):
            mock_response = type('MockResponse', (), {'status_code': 200, 'json': lambda: {}})()
            
            if 'pokemon/' in url:
                mock_response.json = lambda: MOCK_POKEMON_DETAIL
            elif 'pokemon-species/' in url:
                mock_response.json = lambda: MOCK_SPECIES_DATA
                
            return mock_response
            
        mock_get.side_effect = mock_get_side_effect
        
        response = client.get('/pokemon/bulbasaur')
        assert response.status_code == 200
        assert b'bulbasaur' in response.data
