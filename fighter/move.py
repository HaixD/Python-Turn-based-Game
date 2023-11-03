from __future__ import annotations
from dataclasses import dataclass
import functions.bool_evaluation_set as bool_evaluation_set
import fighter.effect as effect

@dataclass(frozen = True)
class Move:
    """Move is a wrapper for effects.

    Move is a wrapper for effects. It includes both a name and a
    requirement for said effects to trigger. Moves should be hidden
    when their requirement(s) are not met.

    Attibutes:
        name (str): The name of this Move.
        effect (Effect): The effect to trigger when this move is used.
        requirement (callable[None, bool]): The callback to tell 
        whether conditions for this Move are satisfied.
    """
    name: str
    effect: effect.Effect
    requirement: callable[None, bool]

    def __bool__(self) -> bool:
        """Returns whether or not this Move is ready.

        Returns:
            bool: Whether or not this Move is ready.
        """
        return self.requirement()

    def __call__(self, target: dict[str, any]) -> None:
        """Triggers the effect if this Move is ready.

        Args:
            target (dict[str, any]): The target to apply the effect 
            on.

        Raises:
            PermissionError: The requirements for this Move are not 
            satisfued (bool(Move) returns False).
        """
        if not bool(self):
            raise PermissionError("The requirements for this Move are not satisfied.")
        
        self.effect(target)

    @staticmethod
    def generate(caster: dict[str, any], name: str, effects: list[dict[str, any]], requirements: list[list[dict[str, any]]]) -> Move:
        """Generates a Move based on the JSON template.

        Generates a Move based on the JSON template. For reference,
        see assets/data/templates/move_template.json to see the 
        expected format.

        Args:
            caster (dict[str, any]): The fighter using this Move.
            name (str): The name of this Move.
            effects (list[dict[str, any]]): The functions to
            execute for this Move/Effect.
            requirements (list[list[dict[str, any]]]): The conditions
            required for this move to be valid.

        Returns:
            The generated Move.
        """
        effect_callback = effect.Effect.generate(caster, effects)
        requirement = bool_evaluation_set.BoolEvaluationSet.generate(caster, requirements)

        return Move(name, effect_callback, requirement)