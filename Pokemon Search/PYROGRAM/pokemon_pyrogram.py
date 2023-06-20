import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from Shikimori import pbot


def get_pokemon_info(name_or_id):
    base_url = "https://sugoi-api.vercel.app/pokemon"
    params = {}

    if isinstance(name_or_id, str):  # Check if name_or_id is a string
        params["name"] = name_or_id
    elif isinstance(name_or_id, int):  # Check if name_or_id is an integer
        params["id"] = name_or_id
    else:
        return None

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()

    return None


@pbot.on_message(filters.command("pokedex"))
async def pokedex(client: Client, message: Message):
    try:
        if len(message.command) > 1:
            pokemon_info = await get_pokemon_info(message.command[1:])
            if pokemon_info:
                pokemon = pokemon_info["name"]
                pokedex_id = pokemon_info["id"]
                height = pokemon_info["height"]
                weight = pokemon_info["weight"]

                abilities = [
                    ability["ability"]["name"] for ability in pokemon_info["abilities"]
                ]

                image_url = pokemon_info["sprites"]["other"]["official-artwork"][
                    "front_default"
                ]
                caption = f"""
======[ 【Ｐｏｋéｄｅｘ】 ]======

╒═══「 **{pokemon.upper()}** 」

**Pokedex ➢** `{pokedex_id}`
**Type ➢** {type}
**Abilities ➢** {abilities}
**Height ➢** `{height}`
**Weight ➢** `{weight}`


"""

                await message.reply_photo(photo=image_url, caption=caption)
            else:
                await message.reply_text("Pokemon not found.")
        else:
            await message.reply_text("Please provide a Pokemon name or ID.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
