def avgStructure(attrs, func, group_variable, indentation, condition):
    
    avg = ""
    target=func
    if '_' in func:
        target=func.split('_')[2]
    group_key = f"group[{attrs}]['{func}']"
    # group_key = "group[" + group_variable + ']["'  + func[0] + '"]'
    count_key = "count_"  + func + "[" + attrs + "]"
    print(f"count_key: {count_key}")

    if condition:
        avg += f'{" " * indentation}if {condition}:\n'
        indentation += 2

    avg += ((" " * indentation) + "if not " + group_key + ":\n")
    indentation += 2
    avg += ((" " * indentation) + group_key + " = " + target  + "\n")
    avg += ((" " * indentation) + count_key + " += 1\n")
    indentation -= 2 

    avg += ((" " * indentation) + "else:\n")
    indentation += 2
    avg += ((" " * indentation) + count_key + " += 1\n")
    avg += ((" " * indentation) + group_key + " += ((" + target  + " - " + group_key + ")/" + count_key + ")\n")

    return avg
# print(avgStructure("(key_cust)",
#       ('0_avg_quant', 'avg', 'quant'), "0", 6, 'group[(key_cust)]["cust"] == cust and quant > group[(key_cust)]["0_avg_quant"]'))


def maxStructure(attrs, func, group_variable_attrs_max_aggregate, index, indentation, condition):

    structure = ""
    group_key = f'group[{attrs}]["{func}"]'
    target=func
    if '_' in func:
        target=func.split('_')[2]
    if condition:
        structure += (" " * indentation) + f'if {condition}:\n'
        indentation += 2

    structure += (" " * indentation) + f'if not {group_key}:\n'
    indentation += 2
    structure += (" " * indentation) + f'{group_key} = {target}\n'

    if group_variable_attrs_max_aggregate:
        for attr in group_variable_attrs_max_aggregate:
            if not index:
                structure += (" " * indentation) + \
                f'{group_attr_key} = {attr.split(".")[1]}\n'
            else: 
                group_attr_key = f'group[{attrs}]["{index}.{attr}"]'
                structure += (" " * indentation) + \
                    f'{group_attr_key} = {attr}\n'

    indentation -= 2
    structure += (" " * indentation) + "else:\n"
    indentation += 2
    structure += (" " * indentation) + f'if {target} > {group_key}:\n'
    indentation += 2
    structure += (" " * indentation) + f'{group_key} = {target}\n'

    if group_variable_attrs_max_aggregate:
        for attr in group_variable_attrs_max_aggregate:
            if not index:
                structure += (" " * indentation) + \
                f'{group_attr_key} = {attr.split(".")[1]}\n'
            else: 
                group_attr_key = f'group[{attrs}]["{index}.{attr}"]'
                structure += (" " * indentation) + \
                    f'{group_attr_key} = {attr}\n'
    return structure
# print(maxStructure("(key_cust)", ('0_max_quant', 'max', 'quant'), None, 6, None))


def minStructure(attrs, func, group_variable_attrs_min_aggregate, index, indentation, condition):
    structure = ""
    group_key = f'group[{attrs}]["{func}"]'
    print(f"group_variable_attrs_min_aggregate:{group_variable_attrs_min_aggregate}")
    target=func
    if '_' in func:
        target=func.split('_')[2]
    if condition:
        structure += (" " * indentation) + f'if {condition}:\n'
        indentation += 2

    structure += (" " * indentation) + f'if not {group_key}:\n'
    indentation += 2
    structure += (" " * indentation) + f'{group_key} = {target}\n'

    if group_variable_attrs_min_aggregate:
        for attr in group_variable_attrs_min_aggregate:
            if not index:
                structure += (" " * indentation) + \
                f'{group_attr_key} = {attr.split(".")[1]}\n'
            else: 
                group_attr_key = f'group[{attrs}]["{attr}"]'
                structure += (" " * indentation) + \
                    f'{group_attr_key} = {attr}\n'

    indentation -= 2
    structure += (" " * indentation) + "else:\n"
    indentation += 2
    structure += (" " * indentation) + f'if {target} < {group_key}:\n'
    indentation += 2
    structure += (" " * indentation) + f'{group_key} = {target}\n'

    if group_variable_attrs_min_aggregate:
        for attr in group_variable_attrs_min_aggregate:
            if not index:
                structure += (" " * indentation) + \
                f'{group_attr_key} = {attr.split(".")[1]}\n'
            else: 
                group_attr_key = f'group[{attrs}]["{index}.{attr}"]'
                structure += (" " * indentation) + \
                    f'{group_attr_key} = {attr}\n'

    return structure
# print(minStructure("(key_cust)", ('0_min_quant', 'min', 'quant'), None, 6, None))


def countStructure(attrs, func, indentation, condition):

    structure = ""
    group_key = f'group[{attrs}]["{func}"]'
    target=func
    if '_' in func:
        target=func.split('_')[2]
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
    group_key = f"group[{attrs}]['{func}']"
    target=func
    if '_' in func:
        target=func.split('_')[2]
    if condition:
        structure += (" " * indentation) + f"if {condition}:\n"
        indentation += 2

    structure += (" " * indentation) + f"if not {group_key}:\n"
    indentation += 2
    structure += (" " * indentation) + f"{group_key} = {target}\n"
    indentation -= 2
    structure += (" " * indentation) + "else:\n"
    indentation += 2
    structure += (" " * indentation) + f"{group_key} += {target}\n"

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
