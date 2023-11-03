# A Python Turn-based Game

I started this project to see how far you can go from using python to interpret some JSON files. This project has been abandoned.

# Getting Started
Run `main.py` to see a demo of what this project is capable of. Enter 'hit' or 'heal' (when available) to choose a move.

## Adding new content

### Functions
Functions are not moves. They do not take a target as a parameter. They insead work with inferred and literal parameters along with the cache. Functions are meant to be used to set up an environment in places like `pre effect`, `post effect`, and `requirements` (within the JSON).

To add new functions, go into `functions/functions.py` and create your function there. Functions should have at least 1 parameter where the first one is the cache of the instance/fighter triggering it. Afterwards, add your function to the global variable `FUNCTIONS` to register it and allow for it to be called from the JSON files.

### Effects
Unlike functions, effects have 2 parts. Initialization (where they are treated as functions), and the call itself. Effects should inherit from `EffectNode` (found in `effects/effect_node.py`). When the effect is invoked (after initialization), it will receive a dictionary as its only parameter. The dictionary is the target's cache. To access the invoker's cache, use `self.cache`.

# Examples (JSON)
## Requirements
```
"requirements": [
    [
        {
            "function": "subtract",
            "inferred parameters": {
                "lhs": "max hp"
            },
            "literal parameters": {
                "rhs": 100,
                "key": "heal hp required"
            },
            "requirements": []
        },
        {
            "function": "compare",
            "inferred parameters": {
                "lhs": "hp",
                "rhs": "heal hp required"
            }, 
            "literal parameters": {
                "operator": "<=",
                "key": "throwaway"
            },
            "requirements": []
        }
    ]
]
```
The requirements above only has a single requirement (that has 2 parts). The first part is the subtract function. The `max hp` attribute/value is passed as the lhs, 100 is passed into `rhs`, and the output is saved in the key `heal hp required`. The python equivalence to this is `subtract(lhs = self.cache['max hp'], rhs = 100, key = 'heal hp required')`; the output is stored to `self.cache[key]` or `self.cache['heal hp required']`. The second part compares the inferred values `hp` and `heal hp required`. If `hp` is less than our equal to `heal hp required` then whatever function/effect that has this requirement will trigger. Note that the key passed is `throwaway`; this is because we do not want to save the output of this compare to a key.

**Requirements should be `[]` in the event that there aren't any*

## Effects
```
"effects": [
    {
        "effect": "damage target",
        "inferred parameters": {
            "min_damage": "base damage",
            "max_damage": "damage cap"
        },
        "literal parameters": {},
        "pre effect": [
            {
                "function": "get target attribute",
                "inferred parameters": {
                    "target_index": "last hit"
                },
                "literal parameters": {
                    "key": "enemy element",
                    "target_key": "element"
                },
                "requirements": []
            },
            {
                "function": "set cache",
                "inferred parameters": {},
                "literal parameters": {
                    "key": "damage doubled",
                    "value": true
                },
                "requirements": [
                    [
                        {
                            "function": "compare",
                            "inferred parameters": {
                                "lhs": "enemy element",
                                "rhs": "strong against"
                            }, 
                            "literal parameters": {
                                "operator": "=",
                                "key": "throwaway"
                            },
                            "requirements": []
                        }
                    ]
                ]
            },
            {
                "function": "add",
                "inferred parameters": {
                    "lhs": "damage cap",
                    "rhs": "base damage"
                },
                "literal parameters": {
                    "key": "damage cap"
                },
                "requirements": [
                    [
                        {
                            "function": "compare",
                            "inferred parameters": {
                                "lhs": "enemy element",
                                "rhs": "strong against"
                            }, 
                            "literal parameters": {
                                "operator": "=",
                                "key": "throwaway"
                            },
                            "requirements": []
                        }
                    ]
                ]
            }
        ],
        "post effect": [     
            {
                "function": "subtract",
                "inferred parameters": {
                    "lhs": "damage cap",
                    "rhs": "base damage"
                },
                "literal parameters": {
                    "key": "damage cap"
                },
                "requirements": [
                    [
                        {
                            "function": "compare",
                            "inferred parameters": {
                                "lhs": "damage doubled"
                            },
                            "literal parameters": {
                                "rhs": true,
                                "operator": "=",
                                "key": "throwaway"
                            },
                            "requirements": []
                        }
                    ]
                ]
            },
            {
                "function": "set cache",
                "inferred parameters": {},
                "literal parameters": {
                    "key": "damage doubled",
                    "value": false
                },
                "requirements": [
                    [
                        {
                            "function": "compare",
                            "inferred parameters": {
                                "lhs": "damage doubled"
                            },
                            "literal parameters": {
                                "rhs": true,
                                "operator": "=",
                                "key": "throwaway"
                            },
                            "requirements": []
                        }
                    ]
                ]
            }
        ],
        "requirements": []
    }
]
```
Above is the JSON resonponsible for damaging a target and putting into account whether the invoker/caster has a type advantage. In summary, the effect damage target takes 2 parameters, a min and max damage whose values will come from 2 inferred variables (variables that are to be looked up within the cache). But before this effect triggers, the type advantage needs to be checked. So in the `pre effect`, we access the target from the `last hit` key (the target this effect is targetting), and we access the target's `element` cache value. The target's element is then checked if it equals the invoker's `strong against` cache value. In the event that they do, `damage doubled` is set to true. Lastly, if the invoker is strong against the target, then their `damage cap` will increase by the `base damage`. Now that `pre effect` has finished execution, the main effect will run; decreasing the target's `hp`. Now the `post effect` will execute. If `damage doubled` is true then we will first subtract the damage cap by base damage to return it to its original value. We then set `damage doubled` back to False.

**In the context of this project, `damage doubled` is a misleading name because the damage cap is not doubled, it is 1.5x what it originally is*