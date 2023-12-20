def avgStructure(attrs, func, group_variable, space, condition):
    
    avg = ""
    target=func
    if '_' in func:
        target=func.split('_')[2]
    group_key = f"group[{attrs}]['{func}']"
    # group_key = "group[" + group_variable + ']["'  + func[0] + '"]'
    count_key = "count_"  + func + "[" + attrs + "]"
    print(f"count_key: {count_key}")

    if condition:
        avg += f'{" " * space}if {condition}:\n'
        space += 2

    avg += ((" " * space) + "if not " + group_key + ":\n")
    space += 2
    avg += ((" " * space) + group_key + " = " + target  + "\n")
    avg += ((" " * space) + count_key + " += 1\n")
    space -= 2 

    avg += ((" " * space) + "else:\n")
    space += 2
    avg += ((" " * space) + count_key + " += 1\n")
    avg += ((" " * space) + group_key + " += ((" + target  + " - " + group_key + ")/" + count_key + ")\n")

    return avg
# print(avgStructure("(key_cust)",
#       ('0_avg_quant', 'avg', 'quant'), "0", 6, 'group[(key_cust)]["cust"] == cust and quant > group[(key_cust)]["0_avg_quant"]'))


def maxStructure(attrs, func, group_variable_attrs_max_aggregate, index, space, condition):

    structure = ""
    group_key = f'group[{attrs}]["{func}"]'
    target=func
    if '_' in func:
        target=func.split('_')[2]
    if condition:
        structure += (" " * space) + f'if {condition}:\n'
        space += 2

    structure += (" " * space) + f'if not {group_key}:\n'
    space += 2
    structure += (" " * space) + f'{group_key} = {target}\n'

    if group_variable_attrs_max_aggregate:
        for attr in group_variable_attrs_max_aggregate:
            if not index:
                structure += (" " * space) + \
                f'{group_attr_key} = {attr.split(".")[1]}\n'
            else: 
                group_attr_key = f'group[{attrs}]["{index}.{attr}"]'
                structure += (" " * space) + \
                    f'{group_attr_key} = {attr}\n'

    space -= 2
    structure += (" " * space) + "else:\n"
    space += 2
    structure += (" " * space) + f'if {target} > {group_key}:\n'
    space += 2
    structure += (" " * space) + f'{group_key} = {target}\n'

    if group_variable_attrs_max_aggregate:
        for attr in group_variable_attrs_max_aggregate:
            if not index:
                structure += (" " * space) + \
                f'{group_attr_key} = {attr.split(".")[1]}\n'
            else: 
                group_attr_key = f'group[{attrs}]["{index}.{attr}"]'
                structure += (" " * space) + \
                    f'{group_attr_key} = {attr}\n'
    return structure
# print(maxStructure("(key_cust)", ('0_max_quant', 'max', 'quant'), None, 6, None))


def minStructure(attrs, func, group_variable_attrs_min_aggregate, index, space, condition):
    structure = ""
    group_key = f'group[{attrs}]["{func}"]'
    print(f"group_variable_attrs_min_aggregate:{group_variable_attrs_min_aggregate}")
    target=func
    if '_' in func:
        target=func.split('_')[2]
    if condition:
        structure += (" " * space) + f'if {condition}:\n'
        space += 2

    structure += (" " * space) + f'if not {group_key}:\n'
    space += 2
    structure += (" " * space) + f'{group_key} = {target}\n'

    if group_variable_attrs_min_aggregate:
        for attr in group_variable_attrs_min_aggregate:
            if not index:
                structure += (" " * space) + \
                f'{group_attr_key} = {attr.split(".")[1]}\n'
            else: 
                group_attr_key = f'group[{attrs}]["{attr}"]'
                structure += (" " * space) + \
                    f'{group_attr_key} = {attr}\n'

    space -= 2
    structure += (" " * space) + "else:\n"
    space += 2
    structure += (" " * space) + f'if {target} < {group_key}:\n'
    space += 2
    structure += (" " * space) + f'{group_key} = {target}\n'

    if group_variable_attrs_min_aggregate:
        for attr in group_variable_attrs_min_aggregate:
            if not index:
                structure += (" " * space) + \
                f'{group_attr_key} = {attr.split(".")[1]}\n'
            else: 
                group_attr_key = f'group[{attrs}]["{index}.{attr}"]'
                structure += (" " * space) + \
                    f'{group_attr_key} = {attr}\n'

    return structure
# print(minStructure("(key_cust)", ('0_min_quant', 'min', 'quant'), None, 6, None))


def countStructure(attrs, func, space, condition):

    structure = ""
    group_key = f'group[{attrs}]["{func}"]'
    target=func
    if '_' in func:
        target=func.split('_')[2]
    if condition:
        structure += (" " * space) + f'if {condition}:\n'
        space += 2

    structure += (" " * space) + f'if not {group_key}:\n'
    space += 2
    structure += (" " * space) + f'{group_key} = 1\n'
    space -= 2
    structure += (" " * space) + "else:\n"
    space += 2
    structure += (" " * space) + f'{group_key} += 1\n'

    return structure
# print(countStructure("(key_cust)", ('0_count_quant', 'count', 'quant'), 6, None))


def sumStructure(attrs, func, space, condition):

    structure = ""
    group_key = f"group[{attrs}]['{func}']"
    target=func
    if '_' in func:
        target=func.split('_')[2]
    if condition:
        structure += (" " * space) + f"if {condition}:\n"
        space += 2

    structure += (" " * space) + f"if not {group_key}:\n"
    space += 2
    structure += (" " * space) + f"{group_key} = {target}\n"
    space -= 2
    structure += (" " * space) + "else:\n"
    space += 2
    structure += (" " * space) + f"{group_key} += {target}\n"

    return structure

# print(sumScript("(key_cust)", ('0_sum_quant', 'sum', 'quant'), 6, None))


def noAggregate(group_attr, attrs, space, condition):
    script = ""

    if condition:
        script += (" " * space) + f"if {condition}:\n"
        space += 2

    for attr in attrs:
        group_key = f"group[{group_attr}]['{attr}']"
        script += (" " * space) + f"{group_key} = {attr.split('.')[1]}\n"

    return script
