from abc import ABC, abstractmethod

class EffectNode(ABC):
    """EffectNode represents a specific kind of callable object.

    EffectNode is a callable class/object that accepts a target.

    Attributes:
        cache (dict[str, any]): The data that this EffectNode was 
        initialized with.
    """
    def __init__(self, cache: dict[str, any]):
        """Initialzes an EffectNode with the given cache data.

        Args:
            cache (dict[str, any]): The data that this EffectNode 
            was initialized with.
        """
        self.cache: dict[str, any] = cache
    
    @abstractmethod
    def __call__(self, target: dict[str, any]) -> None:
        """This method should be overridden to perform any action.

        Args:
            target (dict[str, any]): The target of this function call.

        Raises:
            NotImplemented: This method was not overridden.
        """
        raise NotImplemented()