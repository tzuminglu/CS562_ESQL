def avgStructure(attrs, func, group_variable, indentation, condition):
    structure = ""
    group_key = f"group[{attrs}]"
    count_key = "count_" + group_variable + "_" + func[2] + "[" + attrs + "]"

    if condition:
        structure += ((" " * indentation) + "if " + condition + ":\n")
        indentation += 2

    structure += ((" " * indentation) + count_key +
                  f".get({attrs}), 0) += 1\n")
    structure += ((" " * indentation) + group_key +
                  f"[\"{func[0]}\"] = (({func[2]} + ({count_key} - 1) * {group_key}.get({func[0]}, 0))) / {count_key} \n")
    return structure
# print(avgStructure("(key_cust)",
#       ('0_avg_quant', 'avg', 'quant'), "0", 6, 'group[(key_cust)]["cust"] == cust and quant > group[(key_cust)]["0_avg_quant"]'))


def maxStructure(attrs, func, group_variable_attrs_max_aggregate, indentation, condition):

    structure = ""
    group_key = f'group[{attrs}]["{func[0]}"]'

    if condition:
        structure += (" " * indentation) + f'if {condition}:\n'
        indentation += 2

    structure += (" " * indentation) + f'if not {group_key}:\n'
    indentation += 2
    structure += (" " * indentation) + f'{group_key} = {func[2]}\n'

    if group_variable_attrs_max_aggregate:
        for attr in group_variable_attrs_max_aggregate:
            group_attr_key = f'group[{attrs}]["{attr}"]'
            structure += (" " * indentation) + \
                f'{group_attr_key} = {attr.split(".")[1]}\n'

    indentation -= 2
    structure += (" " * indentation) + "else:\n"
    indentation += 2
    structure += (" " * indentation) + f'if {func[2]} > {group_key}:\n'
    indentation += 2
    structure += (" " * indentation) + f'{group_key} = {func[2]}\n'

    if group_variable_attrs_max_aggregate:
        for attr in group_variable_attrs_max_aggregate:
            group_attr_key = f'group[{attrs}]["{attr}"]'
            structure += (" " * indentation) + \
                f'{group_attr_key} = {attr.split(".")[1]}\n'
    return structure
# print(maxStructure("(key_cust)", ('0_max_quant', 'max', 'quant'), None, 6, None))


def minStructure(attrs, func, group_variable_attrs_min_aggregate, indentation, condition):
    structure = ""
    group_key = f'group[{attrs}]["{func[0]}"]'

    if condition:
        structure += (" " * indentation) + f'if {condition}:\n'
        indentation += 2

    structure += (" " * indentation) + f'if not {group_key}:\n'
    indentation += 2
    structure += (" " * indentation) + f'{group_key} = {func[2]}\n'

    if group_variable_attrs_min_aggregate:
        for attr in group_variable_attrs_min_aggregate:
            group_attr_key = f'group[{attrs}]["{attr}"]'
            structure += (" " * indentation) + \
                f'{group_attr_key} = {attr.split(".")[1]}\n'

    indentation -= 2
    structure += (" " * indentation) + "else:\n"
    indentation += 2
    structure += (" " * indentation) + f'if {func[2]} < {group_key}:\n'
    indentation += 2
    structure += (" " * indentation) + f'{group_key} = {func[2]}\n'

    if group_variable_attrs_min_aggregate:
        for attr in group_variable_attrs_min_aggregate:
            group_attr_key = f'group[{attrs}]["{attr}"]'
            structure += (" " * indentation) + \
                f'{group_attr_key} = {attr.split(".")[1]}\n'

    return structure
# print(minStructure("(key_cust)", ('0_min_quant', 'min', 'quant'), None, 6, None))


def countStructure(attrs, func, indentation, condition):

    structure = ""
    group_key = f'group[{attrs}]["{func[0]}"]'

    if condition:
        structure += (" " * indentation) + f'if {condition}:\n'
        indentation += 2

    structure += (" " * indentation) + f'if not {group_key}:\n'
    indentation += 2
    structure += (" " * indentation) + f'{group_key} = 1\n'
    indentation -= 2
    structure += (" " * indentation) + "else:\n"
    indentation += 2
    structure += (" " * indentation) + f'{group_key} += 1\n'

    return structure
# print(countStructure("(key_cust)", ('0_count_quant', 'count', 'quant'), 6, None))


def sumStructure(attrs, func, indentation, condition):

    structure = ""
    group_key = f"group[{attrs}]['{func[0]}']"

    if condition:
        structure += (" " * indentation) + f"if {condition}:\n"
        indentation += 2

    structure += (" " * indentation) + f"if not {group_key}:\n"
    indentation += 2
    structure += (" " * indentation) + f"{group_key} = {func[2]}\n"
    indentation -= 2
    structure += (" " * indentation) + "else:\n"
    indentation += 2
    structure += (" " * indentation) + f"{group_key} += {func[2]}\n"

    return structure

# print(sumScript("(key_cust)", ('0_sum_quant', 'sum', 'quant'), 6, None))


def noAggregate(group_attr, attrs, indentation, condition):
    script = ""

    if condition:
        script += (" " * indentation) + f"if {condition}:\n"
        indentation += 2

    for attr in attrs:
        group_key = f"group[{group_attr}]['{attr}']"
        script += (" " * indentation) + f"{group_key} = {attr.split('.')[1]}\n"

    return script
