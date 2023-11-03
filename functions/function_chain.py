from __future__ import annotations
import functions.conditional_function as conditional_function
import functions.functions as functions

class FunctionChain:
    """FunctionChain represents a collection of callable objects.

    FunctionChain represents a collection of callable objects. 
    Callable objects are called in the order they appear in the 
    functions list.

    Note:
        return values are ignored because it is unclear which if any
        should be returned

    Attributes:
        function (list[callable[None, None]]): The list of callable
        objects to be executed.
    
    """
    def __init__(self, *functions: callable[None, None]):
        """Initializes a FunctionChain with the given callable objects.

        Arguments: 
            functions (Callable[None, None]): The list of callable
        objects to be executed.
        """
        self.functions: list[callable[None, None]] = list(functions)

    def __call__(self) -> None:
        """Executes all callable objects in the order they appear.

        Executes all callable objects in the order they appear in the
        functions list. Return values are ignored.
        """
        for function in self.functions:
            function()

    @staticmethod
    def generate(functions_list: list[dict[str, any]], data: dict[str, any]) -> FunctionChain:
        """Generates a FunctionChain from the expected JSON data.

        Generates a FunctionChain from the expected JSON data. This
        function will only attempt to create ConditionalFunction(s).
        There may be ConditionalFunction(s) without any condition.

        Note:
            A literal parameter of key/name 'cache' is automatically
            inserted and it stores the data passed into this generate
            function.

        Args:
            functions_list (list[dict[str, any]]): _description_
            data (dict[str, any]): _description_

        Returns:
            FunctionChain: _description_
        """
        generated_functions = []

        for function in functions_list:
            function['literal parameters']['cache'] = data
            generated_functions.append(
                conditional_function.ConditionalFunction.generate(
                    functions.FUNCTIONS[function['function']], 
                    data,
                    function['inferred parameters'],
                    function['literal parameters'],
                    function['requirements']
                )
            )

        return FunctionChain(*generated_functions)