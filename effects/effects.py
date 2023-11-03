from random import randint
import effects.effect_node as effect_node

class DamageTarget(effect_node.EffectNode):
    """DamageTarget represents a basic effect/move that decreases health.

    DamageTarget represents a basic effect/move that decreases health
    by a given range (inclusive).

    Attributes:
        self.min_damage (int): The least amount of health to remove.
        self.max_damage (int): The most amount of health to remove.
    """
    
    def __init__(self, cache: dict[str, any], min_damage: int, max_damage: int):
        """Initializes a DamageTarget with the given min and max damage.

        Args:
            cache (dict[str, any]): The data this DamageTarget was
            initialized with.
            min_damage (int): The least amount of health to remove.
            max_damage (int): The most amount of health to remove.
        """
        super(DamageTarget, self).__init__(cache)
        self.min_damage: int = min_damage
        self.max_damage: int = max_damage

    def __call__(self, target: dict[str, any]) -> None:
        """Removes a randomly generated amount of hp from the target.

        Args:
            target (dict[str, any]): The target cache/data to remove
            hp from.
        """
        target['hp'] -= randint(self.min_damage, self.max_damage)

class HealSelf(effect_node.EffectNode):
    """HealSelf represents a basic effect/move that increases user hp.

    Attributes:
        heal_amount (int): The amount to heal the user by (user will 
        not heal beyond their max hp; no error is thrown if this 
        occurs)
    """

    def __init__(self, cache: dict[str, any], heal_amount: int):
        """Initializes a HealSelf with the given min and heal amount.

        Args:
            heal_amount (int): The amount to heal the user by (user 
            will not heal beyond their max hp; no error is thrown if 
            this occurs)
        """
        super(HealSelf, self).__init__(cache)
        self.heal_amount: int = heal_amount

    def __call__(self, target: dict[str, any]) -> None:
        """Heals user by the given amount.

        Heals user by the given amount. The target parameter is
        ignored.

        Note:
            There should be a way to choose a target (including self)
            in the future. Until then, the target will always be 
            assumed to be the user

        Args:
            target (dict[str, any]): This parameter is meaningless.
        """
        print(id(self.cache))
        self.cache['hp'] = min(self.cache['hp'] + self.heal_amount, self.cache['max hp'])

EFFECTS = {
    "damage target": DamageTarget,
    "heal self": HealSelf
}