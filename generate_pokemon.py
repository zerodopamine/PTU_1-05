import json
import os

pokemon = "Galvantula"
level = "67"
all_moves = True

''' DO NOT EDIT PAST THIS POINT'''
def create_pokemon():
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Load the pokedex
    with open(os.path.join(script_dir, 'pokedex.json'), 'r') as f:
        data = json.load(f)
    # Load the requested pokemon
    try: 
        pokemon_data = data[pokemon.upper()]
    except KeyError: 
        print(f"Cannot find {pokemon} in pokedex, perhaps it has a strange format?")
        return
    # Set the pokemon's level
    pokemon_data["Level"] = str(level)

    '''Load move data'''
    with open(os.path.join(script_dir, 'moves.json'), 'r', encoding="utf8") as f:
        moves = json.load(f)
    move_levels = [int(x.split(" ")[0]) for x in pokemon_data["Moves"]]
    move_names = [" ".join(x.split(" ")[1:]) for x in pokemon_data["Moves"]]
    if not all_moves:
        below_target = [i for i in range(len(move_levels)) if move_levels[i] <= int(pokemon_data["Level"])][-6:]
    else:
        below_target = [i for i in range(len(move_levels))]
    for move_index, index in enumerate(below_target):
        try: pokemon_data[f"Move{move_index}"] = moves[move_names[index]]
        except KeyError:
            print(f'Cannot find {move_names[index]} in move.json')
            continue
        # Add the move name and rename certain keys
        pokemon_data[f"Move{move_index}"]["Name"] = move_names[index]
        pokemon_data[f"Move{move_index}"]["DB"] = pokemon_data[f"Move{move_index}"].pop("Damage Base")
        pokemon_data[f"Move{move_index}"]["DType"] = pokemon_data[f"Move{move_index}"].pop("Class")
        pokemon_data[f"Move{move_index}"]["Freq"] = pokemon_data[f"Move{move_index}"].pop("Frequency")
        pokemon_data[f"Move{move_index}"]["Effects"] = pokemon_data[f"Move{move_index}"].pop("Effect")
        # If the move has no DB change it from N/A to ""
        if pokemon_data[f"Move{move_index}"]["DB"] == "N/A": pokemon_data[f"Move{move_index}"]["DB"] = ""
        # Print frequency so user can quickly fill it out
        print(pokemon_data[f"Move{move_index}"]["Name"], pokemon_data[f"Move{move_index}"]["Freq"])
    # Remove the Moves list from the dict 
    pokemon_data.pop("Moves")

    '''Load ability data'''
    with open(os.path.join(script_dir, 'abilities.json'), 'r', encoding="utf8") as f:
        abilities = json.load(f)
    for ability_index, ability in enumerate(pokemon_data["Abilities"]):
        try: pokemon_data[f"Ability{ability_index+1}"] = abilities[f' {ability}']
        except KeyError:
            print(f'Cannot find {ability} in abilities.json')
            continue
        pokemon_data[f"Ability{ability_index+1}"]["Name"] = ability
        pokemon_data[f"Ability{ability_index+1}"]["Info"] = pokemon_data[f"Ability{ability_index+1}"].pop("Effect")
        pokemon_data[f"Ability{ability_index+1}"]["Freq"] = pokemon_data[f"Ability{ability_index+1}"].pop("Frequency")
    
    print(json.dumps(pokemon_data))

create_pokemon()