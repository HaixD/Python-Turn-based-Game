from __future__ import annotations
import functions.function_node as function_node
import functions.bool_evaluation_set as bool_evaluation_set
from typing import TypeVar

T = TypeVar('T')

class ConditionalFunction:
    """ConditionalFunction represents a callable that has a conditional.

    ConditionalFunction represents a callable (callback) that has a 
    conditional. The callback will not execute if the requirement
    callback returns False. No error is thrown if False is returned
    by the requirement function.


    Attributes:
        function (callable[..., T]): The primary function.
        requirement (callable[None, bool]): The requirement function
        that returns True if the primary function can run and False
        otherwise.
    """
    def __init__(self, function: callable[..., T], requirement: callable[None, bool]):
        """Initializes a ConditonalFunction with the given functions.

        Args:
        function (callable[..., T]): The primary function.
        requirement (callable[None, bool]): The requirement function
        that returns True if the primary function can run and False
        otherwise.
        """
        self.function: callable[..., T] = function
        self.requirement: callable[None, bool] = requirement

    def __call__(self) -> T:
        """Runs the primary function if the requirement is satisfied.

        Runs the primary function if the requirement is satisfied. if
        the requirement is not satisfied, the return value is None.
        This function does not discern the source of the None.

        Returns:
            The return value of the primary function.
        """
        if self.requirement():
            return self.function()

    @staticmethod
    def generate(function: callable[..., T], data: dict[str, any], inferred: dict[str, str], literal: dict[str, any], requirements: list[list[dict[str, any]]]) -> ConditionalFunction:
        """Creates a ConditionalFunction from the expected JSON data.

        Creates a ConditionaFunction from the expected JSON data. See
        assets/templates/move_template.json for details on what the
        expected JSON data is. 

        Note:
            A literal parameter of key/name 'cache' is automatically
            inserted and it stores the data passed into this generate
            function.
        
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
            requirements (list[list[dict[str, any]]]): The 
            requirements for the primary function to be executed.

        Returns:
            The generated ConditionalFunction.
        """
        literal['cache'] = data
        
        return ConditionalFunction(
            function_node.FunctionNode(
                function, 
                lambda : {key: data[value] for key, value in inferred.items()} | literal
            ), bool_evaluation_set.BoolEvaluationSet.generate(
                data,
                requirements
            )
        )