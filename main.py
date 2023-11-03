from random import randint
import fighter.fighter as fighter

class ConsoleTextBuilder:
    def __init__(self):
        """Initializes a ConsoleTextBuilder with no text.
        """
        self.text = []

    def display(self, clear = True) -> None:
        """Prints the stored text.

        Prints the stored text and clears any stored text if desired.

        Args:
            clear (bool, optional): Whether or not to clear the text. 
            Defaults to True.
        """
        print('\n'.join(self.text))
        if clear:
            self.text.clear()

def set_up_1v1(fighter1_path: fighter.Fighter, fighter2_path: fighter.Fighter) -> tuple[fighter.Fighter, fighter.Fighter]:
    """Loads both fighters and makes them challenge each other.

    Loads both fighters and makes them challenge each other. Both 
    fighters will be returned in the order that the paths were 
    passed.

    Args:
        fighter1_path (Fighter): The first fighter to load.
        fighter2_path (Fighter): The second fighter to load.

    Returns:
        The loaded fighters.
    """
    fighter1 = fighter.Fighter.load_json(fighter1_path)
    fighter2 = fighter.Fighter.load_json(fighter2_path)

    fighter1.challenge_target(fighter2)

    return fighter1, fighter2

def is_challenge_active(fighter1: fighter.Fighter, fighter2: fighter.Fighter) -> bool:
    """Checks if fighter1 is still challenging fighter2.

    Checks if fighter1 is still challenging fighter2. The fighters
    are not challenging each other if they arent in each other's 
    target list or at least one of them is dead.

    Args:
        fighter1 (Fighter): One of the challenge participants.
        fighter2 (Fighter): The other challenge participant.

    Returns:
        True if fighter1 is still challenging fighter2 and false 
        otherwise.
    """
    if (fighter1 in fighter2.targets) and (fighter2 in fighter1.targets):
        return fighter1 and fighter2
    return False

def get_challenge_winner(fighter1: fighter.Fighter, fighter2: fighter.Fighter) -> fighter.Fighter | None:
    """Gets the winner of 2 fighters.

    Gets the winner of 2 fighters. This function cannot tell if the 2
    fighters were in a challenge before hand, it only returns the 1
    remaining fighter if possible, and None otherwise.

    Args:
        fighter1 (Fighter): One of the challenge participants.
        fighter2 (Fighter): The other challenge participant.

    Returns:
        The remaining fighter.
    """
    if fighter1 and not fighter2:
        return fighter1
    elif fighter2 and not fighter1:
        return fighter2
    return None

if __name__ == '__main__':
    fighter1, fighter2 = set_up_1v1('assets/data/monsters/dummy1.json', 'assets/data/monsters/dummy2.json')

    console = ConsoleTextBuilder()

    while True:
        #get move from user
        console.text.append('Which move do you want to use?')

        moves = {}
        for index, move in enumerate(fighter1.get_possible_moves()):
            move_name = move.name.lower()
            moves[move_name] = index
            console.text.append(f'{index + 1}. {move_name}')

        console.display()
        fighter1_move_choice = input('>>> ').lower()

        if fighter1_move_choice not in moves:
            console.text.append('Invalid move.')
            continue

        #fighter1 attack fighter2
        fighter2_before_hp = fighter2.cache['hp']
        fighter1.attack(moves[fighter1_move_choice], 0)
        console.text.append(f'target has {fighter2.cache["hp"]}/{fighter2.cache["max hp"]} ({fighter2.cache["hp"] - fighter2_before_hp}) hp')

        if not is_challenge_active(fighter1, fighter2):
            console.display()
            break

        #get move from pc
        fighter2_move_choice = randint(0, len(list(fighter2.get_possible_moves())) - 1)

        #fighter2 attack fighter1
        fighter1_before_hp = fighter1.cache['hp']
        fighter2.attack(fighter2_move_choice, 0)
        console.text.append(f'you have {fighter1.cache["hp"]}/{fighter1.cache["max hp"]} ({fighter1.cache["hp"] - fighter1_before_hp}) hp')

        if not is_challenge_active(fighter1, fighter2):
            console.display()
            break

    print('you win' if get_challenge_winner(fighter1, fighter2) is fighter1 else 'you lose')
