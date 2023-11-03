from __future__ import annotations
import functions.conditional_function as conditional_function
import functions.functions as functions
from enum import Enum, unique, auto

@unique
class BoolEvalType(Enum):
    """BoolEvalType represents different propositional connectives.

    Attributes:
        OR: Returns True if one or more proposition is True.
        AND: Returns True if all propositions are True.
    """
    OR = auto()
    AND = auto()

class BoolEvaluationSet:
    """BoolEvaluationSet represents a collection of propositional callbacks.

    BoolEvaluationSet represents a collection of callbacks that 
    return either True or False. The purpose of this class is to 
    combine the propositions of those callbacks.

    Attributes:
        evaluations (list[callable[None, bool]]): The callbacks to
        obtain propositions from
        eval_type (BoolEvalType): The method to combine propositions
        (or propositional connective). 
    """
    def __init__(self, eval_type: BoolEvalType = BoolEvalType.AND, *evaluations: callable[None, bool]):
        """Initializes a BoolEvaluation set from the connective and callbacks.

        Args:
            eval_type (BoolEvalType, optional): The method to combine 
            propositions. Defaults to BoolEvalType.AND.
            evaluations (tuple[callable[None, bool]]): The callbacks to
            obtain propositions from
        """
        self.evaluations: list[callable[None, bool]] = list(evaluations)
        self.eval_type: BoolEvalType = eval_type

    def __bool__(self) -> bool:
        """Returns the combined value of the callback propositions.

        Returns:
            The combined value of the callback propositions.
        """
        if not self.evaluations:
            return True
        
        if self.eval_type == BoolEvalType.AND:
            for evaluation in self.evaluations:
                if evaluation() is False: return False
            return True
        else:
            for evaluation in self.evaluations:
                if evaluation() is True: return True
            return False
        
    def __call__(self):
        """Returns the combined value of the callback propositions.

        This function is interchangeable with using 
        bool(BoolEvaluationSet).

        Returns:
            The combined value of the callback propositions.
        """
        return bool(self)
        
    @staticmethod
    def generate(data: dict[str, any], requirements: list[list[dict[str, any]]]) -> BoolEvaluationSet:
        """Creates a BoolEvaluationSet from the expected JSON data.

        Creates a BoolEvaluationSet from the expected JSON data.
        All statements within the nested list use the AND connective
        while the OR connective is used with said nested list. So if 
        you want to use the OR connective, put only 1 statement in
        each nested list.

        Note:
            A literal parameter of key/name 'cache' is automatically
            inserted and it stores the data passed into this generate
            function.

        Args:
            data (dict[str, any]): The dictionary that parameters are 
            sourced from.
            requirements (list[list[dict[str, any]]]): The 
            requirement function(s) JSON data to execute.

        Returns:
            BoolEvaluationSet: _description_
        """
        generated_requirements = []

        for requirement_set in requirements:
            generated_requirements.append(BoolEvaluationSet(BoolEvalType.AND))
            for requirement in requirement_set:
                requirement['literal parameters']['cache'] = data
                generated_requirements[-1].evaluations.append(
                    conditional_function.ConditionalFunction.generate(
                        functions.FUNCTIONS[requirement.pop('function')], 
                        data, 
                        requirement['inferred parameters'], 
                        requirement['literal parameters'],
                        requirement['requirements']
                    )
                )

        return BoolEvaluationSet(BoolEvalType.OR, *generated_requirements)