import aiohttp
import random

class Pokemon:
    pokemons = {}
    points = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
            # Yeni kullanıcıya 0 başlangıç puanı ver
            if pokemon_trainer not in Pokemon.points:
                Pokemon.points[pokemon_trainer] = 0
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return f"Pokémonunuzun ismi: (İsim için !guess ile oyunu oyna)"

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['sprites']['front_default']
                return None
