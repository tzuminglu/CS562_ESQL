# Using queue to perform the input parser
from collections import deque

def input_parser(file):

    # Apply a dictionary for storing the values
    function_dict = {}
    function_type = ["SELECT ATTRIBUTE(S):",
                     "NUMBER OF GROUPING VARIABLES(n):",
                     "GROUPING ATTRIBUTES(V):",
                     "F-VECT([F]):",
                     "SELECT CONDITION-VECT([σ]):",
                     "HAVING_CONDITION(G):"]
    for key in function_type:
        if key not in function_dict:
            function_dict[key] = list()

    # Use the split method to transform a text file into a list.
    file_list = deque(file.split("\n"))
    while file_list:
        first_pop_text = file_list.popleft()
        if first_pop_text in function_dict:
            second_pop_text = file_list.popleft()
            function_dict[first_pop_text] = second_pop_text
        else:
            raise (ValueError(f"{first_pop_text} doesn't exist"))

    # Split the value using a comma and convert it from a string to a list.
    for key, value in function_dict.items():
        value = value.split(", ")
        function_dict[key] = value
    return function_dict
