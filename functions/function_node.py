from __future__ import annotations
from typing import TypeVar

T = TypeVar('T')

class FunctionNode:
    """FunctionNode represents a callable with indirectly pased parameters.

    FunctionNode represents a callable with indirectly pased 
    parameters. The first callable (function) is supposed to
    be the primary function, while the second callable
    (kwarg_getter) should return a dictionary that will be unpacked
    and passed into the primary function.

    Attributes:
        function (callable[..., T]): The primary function (callback).
        kwarg_getter (callable[None, dict][str, any]): The function 
        used to obtain the parameters.
    """
    def __init__(self, function: callable[..., T], kwarg_getter: callable[None, dict[str, any]]):
        """Initializes a FunctionNode with the given functions.

        Args:
            function (callable[..., T]): The callback.
            kwarg_getter (callable[None, dict[str, any]]): The 
            function used to obtain the parameters.
        """
        self.function: callable[..., T] = function
        self.kwarg_getter: callable[None, dict[str, any]] = kwarg_getter

    def __call__(self) -> T:
        """Calls the callback and returns its return value.

        Returns:
            The callback's return value.
        """
        return self.function(**self.kwarg_getter())
    
    @staticmethod
    def generate(function: callable[..., T], data: dict[str, any], inferred: dict[str, str], literal: dict[str, any]) -> FunctionNode:
        """Creates a FunctionNode from the expected JSON data.

        Creates a FunctionNode from the expected JSON data. This 
        method should not be called unless you know what you are 
        doing. Instead, use ConditionalFunction. See
        assets/templates/move_template.json for details on what the
        expected JSON data is. 

        Args:
            function (callable[..., T]): The primary function.
            data (dict[str, any]): The dictionary that inferred 
            parameters are sourced from.
            inferred (dict[str, str]): The inferred parameters
            (inferred's dict values will be used as keys to obtain
            their new value from data and inferred's dict keys will
            remain the same) that are passed into the function.
            literal (dict[str, any]): literal parameters (those that 
            do not come from data) to pass into the function.

        Returns:
            FunctionNode: The generated FunctionNode.
        """
        return FunctionNode(
            function, 
            lambda : {key: data[value] for key, value in inferred.items()} | literal
        )