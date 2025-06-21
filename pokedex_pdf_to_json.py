import json
import re
import pdfplumber

class extract_pokemon_data:
    def __init__(self, data):
        # Store data
        self.data = data
        # Create a generic pokemon dictionary to store data
        self.pokemon = {
            "EXPORTER_VERSION": "Pokesheets",
            "CharType": 0,
            "nickname": "",
            "species": "",
            "type1": "",
            "type2": "None",
            "Level": "1",
            "HeldItem": "None",
            "Gender": "Male",
            "Nature": "",
            "height": "",
            "weight": "",
            "weightClass": "1",
            "injuries": "0",
            "tempHitPoints": "0",
            "base_HP": "1",
            "base_ATK": "1",
            "base_DEF": "1",
            "base_SPATK": "1",
            "base_SPDEF": "1",
            "base_SPEED": "1",
            "Capabilities": {
                "Overland": 1,
                "Swim": 1,
                "LJ": 1,
                "HJ": 1,
                "Power": 1
            },
            "Athletics": 0,
            "Acrobatics": 0,
            "Charm": 0,
            "Combat": 0,
            "Command": 0,
            "GeneralEducation": 0,
            "MedicineEducation": 0,
            "OccultEducation": 0,
            "PokemonEducation": 0,
            "TechnologyEducation": 0,
            "Focus": 0,
            "Guile": 0,
            "Intimidate": 0,
            "Intuition": 0,
            "Perception": 0,
            "Stealth": 0,
            "Survival": 0,
            "Athletics_bonus": 0,
            "Acrobatics_bonus": 0,
            "Charm_bonus": 0,
            "Combat_bonus": 0,
            "Command_bonus": 0,
            "GeneralEducation_bonus": 0,
            "MedicineEducation_bonus": 0,
            "OccultEducation_bonus": 0,
            "PokemonEducation_bonus": 0,
            "TechnologyEducation_bonus": 0,
            "Focus_bonus": 0,
            "Guile_bonus": 0,
            "Intimidate_bonus": 0,
            "Intuition_bonus": 0,
            "Perception_bonus": 0,
            "Stealth_bonus": 0,
            "Survival_bonus": 0,
            "Abilities" : [],
            "Moves" : []
        }
        # At the very least add the name of the pokemon
        self.pokemon["species"] = self.data[0].strip()
        self.pokemon["nickname"] = self.data[0].strip()
        # Attempt to extract the various bits of pokemon data
        try: self.extract_basic_data()
        except: print(f'{self.pokemon["species"]} issue extracting basic data')
        try: self.extract_capability_list()
        except: print(f'{self.pokemon["species"]} issue extracting capability data')
        try: self.extract_skill_list()
        except: print(f'{self.pokemon["species"]} issue extracting skill data')
        try: self.extract_move_list()
        except: print(f'{self.pokemon["species"]} issue extracting move data')

    def split_by_colon(self, string : str) -> str:
        return string.split(":")[-1].strip()

    def return_int(self, string : str, search_term : str) -> int:
        # In case the PDF is missing a comma find the search term
        string = string[string.index(search_term):]
        try: 
            number = int(string.strip().split(' ')[1])
        except ValueError: 
            print(f'{self.pokemon["species"]} cannot extract {search_term}')
            number = 1
        return number

    def return_int_from_slash(self, string : str, index : int) -> int:
        try:
            number = int(string.strip().split(' ')[1].split('/')[index])
        except IndexError:
            print(f"Error extracting Jump in {self.pokemon["species"]}")
            number = 1
        return number

    def return_int_from_d6(self, string : str, skill : str) -> None:
        self.pokemon[skill] = int(string[string.rindex(" "):string.rindex("d")])
        if "+" in string:
            self.pokemon[f"{skill}_bonus"] = int(string[string.rindex("+")+1:])
    
    def extract_basic_data(self) -> None:
        ''' BASIC DATA'''
        for line in self.data:
            # Base stats
            if "HP:"                in line : self.pokemon["base_HP"]    = self.split_by_colon(line)
            elif "Attack:"          in line : self.pokemon["base_ATK"]   = self.split_by_colon(line)
            elif "Defense:"         in line : self.pokemon["base_DEF"]   = self.split_by_colon(line)
            elif "Special Attack:"  in line : self.pokemon["base_SPATK"] = self.split_by_colon(line)
            elif "Special Defense:" in line : self.pokemon["base_SPDEF"] = self.split_by_colon(line)
            elif "Speed:"           in line : self.pokemon["base_SPEED"] = self.split_by_colon(line)
            # Size Information
            elif "Height :"         in line : self.pokemon["height"]     = self.split_by_colon(line)
            elif "Weight :"         in line : self.pokemon["weight"]     = self.split_by_colon(line)
            # Abilities
            elif "Ability"          in line : self.pokemon["Abilities"].append(self.split_by_colon(line))
            #  Type
            elif "Type :"           in line :
                ptype = self.split_by_colon(line)
                if " / " not in ptype : self.pokemon["type1"] = ptype
                else:
                    self.pokemon["type1"] = ptype.split("/")[0].strip()
                    self.pokemon["type2"] = ptype.split("/")[1].strip()
            # Stop checking lines after size information
            elif "Breeding"         in line : break

    def extract_capability_list(self) -> None:
        ''' CAPABILITY LIST'''
        # Find indices containing search terms
        idx_1 = next(i for i, item in enumerate(self.data) if "Capability List" in item)
        idx_2 = next(i for i, item in enumerate(self.data) if "Skill List" in item)
        capabilities = ' '.join(self.data[idx_1+1:idx_2])
        # Split by comma peceded by a digit "5," or a comma preceded by a closing parenthesis "),"
        capabilities = re.split(r',\s*(?![^()]*\))', capabilities)
        for line in capabilities:
            line = line.strip()
            if "Overland"   in line : self.pokemon["Capabilities"]["Overland"] = self.return_int(line, "Overland")
            elif "Swim"     in line : self.pokemon["Capabilities"]["Swim"]     = self.return_int(line, "Swim")
            elif "Power"    in line : self.pokemon["Capabilities"]["Power"]    = self.return_int(line, "Power")
            elif "Levitate" in line : self.pokemon["Capabilities"]["Levitate"] = self.return_int(line, "Levitate")
            elif "Burrow"   in line : self.pokemon["Capabilities"]["Burrow"]   = self.return_int(line, "Burrow")
            elif "Sky"      in line : self.pokemon["Capabilities"]["Sky"]      = self.return_int(line, "Sky")
            elif "Jump"     in line : 
                self.pokemon["Capabilities"]["LJ"] = self.return_int_from_slash(line, 1)
                self.pokemon["Capabilities"]["HJ"] = self.return_int_from_slash(line, 0)
            else:
                if "Naturewalk" in line:
                    # If there is only a single type of naturewalk
                    if ',' not in line: self.pokemon["Capabilities"][line] = True
                    # If there are multiple nature walks split them up
                    for subcategory in line[line.index('(')+1:line.index(")")].split(','):
                        self.pokemon["Capabilities"][f'Naturewalk ({subcategory.strip()})'] = True
                else:
                    self.pokemon["Capabilities"][line] = True

    def extract_skill_list(self) -> None:
        '''SKILL LIST'''
        # Find indices containing search terms
        idx_1 = next(i for i, item in enumerate(self.data) if "Skill List" in item)
        idx_2 = next(i for i, item in enumerate(self.data) if "Move List" in item)
        skills = ' '.join(self.data[idx_1+1:idx_2])
        # Find malformed data (3d6,+3) and change to proper format (3d6+3,)
        skills = re.sub(r'(\d+d6),\+(\d+)', r'\1+\2,', skills)
        # Split by comma proceded by a digit to accomodate the pdf having errors :upside_down:
        skills = re.split(r'(?<=\d),\s*', skills)
        for line in skills:
            line = line.strip()
            if "Athl"      in line : self.return_int_from_d6(line, "Athletics")
            if "Acro"      in line : self.return_int_from_d6(line, "Acrobatics")
            if "Combat"    in line : self.return_int_from_d6(line, "Combat")
            if "Stealth"   in line : self.return_int_from_d6(line, "Stealth")
            if "Percep"    in line : self.return_int_from_d6(line, "Perception")
            if "Focus"     in line : self.return_int_from_d6(line, "Focus")
            if "Edu: Tech" in line : self.return_int_from_d6(line, "TechnologyEducation")

    def extract_move_list(self) -> None:
        '''MOVE LIST'''
        # Find all instances of "Move List"
        move_lists = [x for x in self.data if "Move List" in x]
        # Use the 2nd and 3rd instances to get the level up moves
        if len(move_lists) > 2:
            moves = self.data[self.data.index(move_lists[1])+1:self.data.index(move_lists[2])]
        # For pokemon with no tm/hm/tutor moves, i.e wobbuffet
        else:
            moves = self.data[self.data.index(move_lists[1])+1:]
        # Use regex to find number followed by space up to a dash
        parsed_moves = []
        for move in moves:
            try: parsed_moves.append(re.search(r'(\d+ .+?)-+\s', move).group(1).strip())
            # PDF is sometimes missing the move type just because...
            except AttributeError: parsed_moves.append(re.search(r'(\d+ .+)', move).group(1).strip())
        self.pokemon["Moves"] = parsed_moves

def extract_pdf_page(pdf, page_number : int) -> list:
    '''Extract a specific page from the PDF'''
    page = pdf.pages[page_number]
    # Get the page width and height to determine column coordinates
    page_width = page.width
    page_height = page.height

    # Define bounding boxes for left and right columns (adjust these values as needed)
    left_bbox = (25, 0, page_width / 2, page_height)  # (x0, y0, x1, y1)
    right_bbox = ((page_width / 2) - 5, 0, page_width, page_height)

    # Extract text for left column
    left_text = page.within_bbox(left_bbox).extract_text()

    # Extract text for right column
    right_text = page.within_bbox(right_bbox).extract_text()

    # Merge str data
    data = f'{left_text}\n{right_text}'
    # Replace words split across lines
    data = data.replace("-\n", "")
    data = data.split("\n")
    return data

data = {}
with pdfplumber.open(r"/home/zero/pCloudDrive/Pokemon/PTU 1.05/Pokedex 1.05.pdf") as pdf:
    for page_number in range(11,744):
        extracted_data = extract_pdf_page(pdf, page_number)
        pokedex = extract_pokemon_data(extracted_data)
        data[pokedex.pokemon["species"]] = pokedex.pokemon

json_file = r"/home/zero/Documents/pokedex.json"
with open(json_file, 'w') as f:
    json.dump(data, f, indent=2)