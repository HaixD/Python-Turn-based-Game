from __future__ import annotations
import json
import functions.function_chain as function_chain
import fighter.move as move

class Fighter:
    """Fighter represents an active participant in the game.

    Fighter is a wrapper/manager for the underlying JSON that it is
    built from. It is important that this class does not abandon the
    use of dictionaries.

    Reserved cache attributes:
        max_hp (int): The upper hp limit of this Fighter.
        hp (int): The current hp of this Fighter.
        name (str): The name of this Fighter.
        moves (list[Move]): A reference to the moves attribute. Do 
        not access this data through the cache, use the attribute
        instead.
        targets (list[Fighter]): A reference to the targets 
        attribute. Do not access this data trhough the cache,
        use the targets attribute instead.
        last hit (int): The index of the target who is being
        targetted. This value is -1 if no target is selected.
    
    Attributes:
        cache (dict[str, any]): The "JSON" that this class manages.
        moves (list[Move]): The list of moves this Fighter can
        use.
        targets (list[Fighter]): All other Fighter(s) this class can
        target.
    
    """
    def __init__(self, name: str, max_hp: int, cache: dict[str, any] = None, moves: list[move.Move] = None):
        """Initializes a Fighter with basic information.

        Args:
            name (str): The name of this Fighter.
            max_hp (int): The upper hp limit of this Fighter.
            cache (dict[str, any], optional): The "JSON" that this 
            class manages.
            moves (list[move.Move], optional): The list of moves 
            this Fighter can use.
        """
        self.cache: dict[str, any] = cache or {}
        self.moves: list[move.Move] = moves or []
        self.targets: list[Fighter] = []

        self.__reserve_cache('max hp', max_hp)
        self.__reserve_cache('hp', max_hp)
        self.__reserve_cache('name', name)
        self.__reserve_cache('moves', self.moves)
        self.__reserve_cache('targets', self.targets)
        self.__reserve_cache('last hit', -1)

    @staticmethod
    def load_json(path: str) -> Fighter:
        """Loads a Fighter from a given JSON file.

        Loads a Fighter from a given JSON file. See
        assets/templates/monster_template.json for reference on how
        a Fighter JSON should look like.

        Args:
            path (str): The relative or absolute path to the JSON.

        Returns:
            The generated Fighter object.
        """
        with open(path, 'r') as file:
            data = json.load(file)

        fighter = Fighter(data['name'], data['max health'], data['cache'])

        for move_params in data['moves']:
            fighter.moves.append(
                move.Move.generate(
                    fighter.cache, 
                    move_params['name'],
                    move_params['effects'],
                    move_params['requirements']
                )
            )

        function_chain.FunctionChain.generate(data['post init'], fighter.cache)()

        return fighter

    def __bool__(self) -> bool:
        """Returns a bool regarding whether this Fighter is alive.

        Returns True if this Fighter is alive, and False otherwise.
        In situations where it does not make sense for a Fighter to
        have hp, just make sure the hp value stays above 0 no matter
        what.

        Returns:
            A bool regarding whether this Fighter is alive.
        """
        return self.cache['hp'] > 0
    
    def __reserve_cache(self, key: str, value: any) -> None:
        """Reserves a key in the cache.

        Reserves a key in the cache. This function does not control
        who/what changes the underlying data of the given key. It 
        only ensures a key exists due to this function.

        Args:
            key (str): The key to reserve.
            value (any): The value stored at the key.

        Raises:
            ValueError: The key already exists prior to this function
            executing.
        """
        if key in self.cache:
            raise ValueError(f'Cache key \'{key}\' is reserved')
        
        self.cache[key] = value

    def on_challenge_end(self):
        if not self.targets:
            return
        
        targets_copy = self.targets.copy()
        self.targets.clear()

        for target in targets_copy:
            target.on_challenge_end()

    def attack(self, move_index: int, target_index: int) -> None:
        """Uses a Move on a target Fighter.

        Uses a Move on a target Fighter. If any target or this 
        Fighter is deemed dead, the targets list of this Fighter
        will be cleared.

        Note:
            This function should only not print text when a GUI is
            implemented.

        Args:
            move_index (int): The index of the move to use.
            target_index (int): The index of the target to attack.
        """
        self.cache['last hit'] = target_index
        self.moves[move_index](self.targets[target_index].cache)

        if not (self and any(self.targets)):
            self.on_challenge_end()

    def get_possible_moves(self) -> tuple[move.Move]:
        """Returns a list of all available moves.

        Returns a list of all available moves.

        Returns:
            A list of all available moves.
        """
        return (move for move in self.moves if move.requirement())

    def challenge_target(self, other: Fighter) -> None:
        """Adds each Fighter to the other's target list.

        Adds a target to the targets list and adds this Fighter to 
        the target's list of targets.

        Args:
            other (Fighter): The Fighter to target.
        """
        self.targets.append(other)
        other.targets.append(self)