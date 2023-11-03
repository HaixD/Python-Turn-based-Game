from __future__ import annotations
from dataclasses import dataclass
import functions.conditional_function as conditional_function
import effects.effects as effects
import effects.effect_node as effect_node
import functions.function_chain as function_chain

class Effect:
    """Effect represents a collection of EffectGroups.

    Effect represents a collection of EffectGroups, each contains a 
    pre-effect, post-effect, and the main effect itself. The 
    pre-effect function(s) execute before the main effect. Then the 
    main effect will execute. Lastly, the post-effect function(s) 
    will execute. There can only be one function running per effect. 
    With that said, effects is a collection of collectionsw where 
    group of 3 has its own pre-effect, main effect, and post-effect.

    Attributes:
        effects (tuple[tuple[callable[None, None], callable[[dict[str, any], dict[str, any]], None], callable[None, None]]]):
        all pre-effects, main effects, and post-effects to run in order.
    
    """

    @dataclass(frozen = True)
    class EffectGroup:
        """EffectGroup represents a collection of 3 callbacks.

        EffectGroup represents a collection of 3 callbacks. A 
        pre-effect, post-effect, and the main effect itself. The 
        pre-effect function(s) execute before the main effect. Then 
        the main effect will execute. Lastly, the post-effect 
        function(s) will execute. There can only be one function 
        running per effect.

        pre_effect (callable[None, None]): The effect(s) to run 
        before the main effect.
        main_effect (callable[dict[str, any], dict[str, any]]): The
        main effect.
        post_effect (callable[None, None]): The effect(s) to run 
        after the main effect.

        """
        
        pre_effect: callable[None, None]
        main_effect: type[effect_node.EffectNode]
        post_effect: callable[None, None]

        def __call__(self, target: dict[str]) -> None:
            """Triggers this EffectGroup.

            Args:
                target (dict[str]): The target to apply effect group 
                on.
            """
            self.pre_effect()
            self.main_effect()(target)
            self.post_effect()
    
    def __init__(self, *effects: Effect.EffectGroup):
        """Initializes an Effect from a collection of 3 callbacks.
        """
        self.effects: tuple[Effect.EffectGroup] = effects

    def __call__(self, target: dict[str, any]) -> None:
        """Triggers the pre-effects, main effects, and post-effects.

        Triggers the pre-effects, main effects, and post-effects in
        the order they are in the tuple. Only the main effect will 
        know who the target is.

        Args:
            target (dict[str, any]): The target to cast an effect on.
        """
        for effect in self.effects:
            effect(target)
    
    @staticmethod
    def generate(caster: dict[str, any], effects_list: list[dict[str, any]]) -> Effect:
        """Generates an effect based on the JSON template.

        Generates an effect based on the JSON template. For reference,
        see assets/data/templates/move_template.json to see the 
        expected format.

        Args:
            caster (dict[str, any]): The fighter casting this effect.
            effects_list (list[dict[str, any]]): The functions to
            execute for this effect.

        Returns:
            The generated Effect.
        """
        generated_effects = []
        
        for effect in effects_list:
            name = effect.pop('effect')

            pre_effect = function_chain.FunctionChain.generate(effect.pop('pre effect'), caster)
            post_effect = function_chain.FunctionChain.generate(effect.pop('post effect'), caster)
            generated_effect = conditional_function.ConditionalFunction.generate(
                effects.EFFECTS[name], 
                caster, 
                effect['inferred parameters'], 
                effect['literal parameters'], 
                effect['requirements']
            )
            
            generated_effects.append(Effect.EffectGroup(pre_effect, generated_effect, post_effect))

        return Effect(*generated_effects)