import requests


def get_pokemon_info(name_or_id):
    base_url = "https://sugoi-api.vercel.app/pokemon"
    params = {}

    if isinstance(name_or_id, str):
        params["name"] = name_or_id
    elif isinstance(name_or_id, int):
        params["id"] = name_or_id
    else:
        return None

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()

    return None
