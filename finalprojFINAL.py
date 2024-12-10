
import argparse
import random
import pandas as pd
# load File 
def load_pokemon_data(file_path):
    """
    Load the Pokémon dataset from a given file path.

    Args:
        file_path (str): Path to the Pokémon dataset CSV file.

    Returns:
        DataFrame: A Pandas DataFrame containing Pokémon data.
    """
    return pd.read_csv(file_path)

# Function for scaling stats (Author: Samuel Adu)
def scale_stats(base_stats, level):
    """
    Scale Pokémon stats based on their level.

    Args:
        base_stats (dict): A dictionary containing base stats (e.g., hp, attack, defense, speed).
        level (int): The level of the Pokémon.

    Returns:
        dict: A dictionary containing the scaled stats.
    """
    scale_factor = level / 50  # Assuming base stats are for Level 50
    return {stat: int(value * scale_factor) for stat, value in base_stats.items()}

# Function for type effectiveness (Author: Carlton Carter)
def get_type_effectiveness(attacker_type, defender_type):
    """
    Calculate type effectiveness multiplier between two Pokémon.

    Args:
        attacker_type (str): The type of the attacking Pokémon.
        defender_type (str): The type of the defending Pokémon.

    Returns:
        float: The type effectiveness multiplier (e.g., 2.0 for super effective, 0.5 for not effective).
    """
    effectiveness_chart = {
        ("Fire", "Grass"): 2.0, ("Grass", "Water"): 2.0, ("Water", "Fire"): 2.0,
        ("Grass", "Fire"): 0.5, ("Water", "Grass"): 0.5, ("Fire", "Water"): 0.5,
    }
    return effectiveness_chart.get((attacker_type, defender_type), 1.0)

# Pokémon Class (Author: Samuel Adu)
class Pokemon:
    """
    Represents a Pokémon with its attributes and behaviors.

    Attributes:
        name (str): The name of the Pokémon.
        type (str): The type of the Pokémon (e.g., Fire, Water, Grass).
        level (int): The level of the Pokémon.
        hp (int): The current hit points of the Pokémon.
        attack (int): The attack stat of the Pokémon.
        defense (int): The defense stat of the Pokémon.
        speed (int): The speed stat of the Pokémon.
    """
    def __init__(self, name, p_type, level, hp, attack, defense, speed):
        self.name = name
        self.type = p_type
        self.level = level
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def is_fainted(self):
        return self.hp <= 0

    def __str__(self):
        return f"{self.name} ({self.type}) - Level {self.level}: HP={self.hp}, attack={self.attack}, defense={self.defense}, speed={self.speed}"

# Function to select a random Pokémon (Author: Carlton Carter)
def select_random_pokemon(pokemon_data):
    """
    Select a random Pokémon from the dataset and scale its stats based on a random level.

    Args:
        pokemon_data (DataFrame): A DataFrame containing Pokémon data.

    Returns:
        Pokemon: A randomly selected Pokémon instance.
    """
    random_pokemon = pokemon_data.sample(n=1).iloc[0]
    level = random.randint(30, 70)  # Randomize levels between 30 and 70
    stats = scale_stats(
        {"hp": random_pokemon["hp"], "attack": random_pokemon["attack"], 
         "defense": random_pokemon["defense"], "speed": random_pokemon["speed"]},
        level
    )
    return Pokemon(
        name=random_pokemon["name"],
        p_type=random_pokemon["type1"],
        level=level,
        hp=stats["hp"],
        attack=stats["attack"],
        defense=stats["defense"],
        speed=stats["speed"]
    )

# Function to conduct a battle (Author: Samuel Adu)
def battle(pokemon1, pokemon2, show_sequence=True):
    """
    Conduct a battle between two Pokémon.

    Args:
        pokemon1 (Pokemon): The first Pokémon.
        pokemon2 (Pokemon): The second Pokémon.
        show_sequence (bool): Whether to show the detailed fight sequence.

    Returns:
        Pokemon: The winner of the battle.
    """
    print(f"\nBattle Start: {pokemon1.name} vs {pokemon2.name}")
    if show_sequence:
        print(pokemon1)
        print(pokemon2)

    if pokemon1.speed > pokemon2.speed:
        first, second = pokemon1, pokemon2
    else:
        first, second = pokemon2, pokemon1

    while not pokemon1.is_fainted() and not pokemon2.is_fainted():
        # First Pokémon attacks
        damage = max(1, (first.attack - second.defense) * get_type_effectiveness(first.type, second.type))
        second.take_damage(damage)
        if show_sequence:
            print(f"{first.name} attacks {second.name} for {damage:.2f} damage. {second.name} hp={second.hp}")
        if second.is_fainted():
            break

        # Second Pokémon attacks
        damage = max(1, (second.attack - first.defense) * get_type_effectiveness(second.type, first.type))
        first.take_damage(damage)
        if show_sequence:
            print(f"{second.name} attacks {first.name} for {damage:.2f} damage. {first.name} hp={first.hp}")
        if first.is_fainted():
            break

    winner = first if not first.is_fainted() else second
    if not show_sequence:
        print(f"Winner: {winner.name}")
    return winner

# Tournament Function (Author: Carlton Carter)
def tournament(pokemon_data, show_sequence=True):
    """
    Conduct a Pokémon tournament with 4 randomly selected Pokémon.

    Args:
        pokemon_data (DataFrame): Pokémon dataset.
        show_sequence (bool): Whether to show fight sequences.
    """
    print("Welcome to the Pokémon Tournament!")
    players = [select_random_pokemon(pokemon_data) for _ in range(4)]
    print("\nRound 1:")
    winner1 = battle(players[0], players[1], show_sequence)
    winner2 = battle(players[2], players[3], show_sequence)
    
    print("\nFinals:")
    champion = battle(winner1, winner2, show_sequence)
    print(f"\nChampion of the Tournament: {champion.name}")

# Main Function (Author: Samuel Adu)
def main():
    parser = argparse.ArgumentParser(description="Pokémon Battle Simulator")
    parser.add_argument("--file", type=str, default="pokemon.csv", help="Path to the Pokémon dataset CSV file")
   #show the fight details or not 
    parser.add_argument("--show_fight", action="store_true", help="Toggle to show the fight sequence, will be store_true or store_false")
    args = parser.parse_args()

    pokemon_data = load_pokemon_data(args.file)
    print("\nLoaded Pokémon Dataset:")
   
    
    tournament(pokemon_data, show_sequence=args.show_fight)

# Run the main function
if __name__ == "__main__":
    main()
