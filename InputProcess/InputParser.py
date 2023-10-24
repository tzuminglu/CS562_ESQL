# using queue to perform the input parser
from collections import deque

def input_parser(file):

    # create a function dictionary for storing the corresponded values
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

    # using split to convert text file into a list in order to put the value into corresponded values
    file_list = deque(file.split("\n"))
    while file_list:
        first_pop_text = file_list.popleft()
        if first_pop_text in function_dict:
            second_pop_text = file_list.popleft()
            function_dict[first_pop_text] = second_pop_text
        else:
            raise (ValueError(f"{first_pop_text} doesn't exist"))

    # split the value by using comma and convert the value from string to list
    for key, value in function_dict.items():
        value = value.split(", ")
        function_dict[key] = value
    return function_dict


file = None
with open("../Test Data/query_input1.txt") as my_file:
    file = my_file.read()
print(file)
print(input_parser(file))
