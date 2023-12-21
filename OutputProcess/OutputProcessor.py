
from coreProcess.GV_process import *
from OutputProcess.AggregationProcessor import *
import sys
sys.path.append('../')


# This function retrieves data from the specified query table.
def outputQueryTable(table_name, space):
    output = ("\n" + (" " * space) +
              f"query = 'select * from {table_name}'\n")
    output += ((" " * space) + "cursor.execute(query)\n")
    output += ((" " * space) + "rows = cursor.fetchall()\n")
    return output


def outputMFStructure(structure, space):
    output = ((" " * space) + "mf_structure = ")
    output += (str(structure) + "\n")
    output += ((" " * space) +
               "group = collections.defaultdict(lambda: dict(mf_structure))\n")

    return output


def firstScan(V, schema, structure, space, aggregate_set):
    """
    The function generates the script for the initial scan. 
    This scan populates the hashmap with grouping attributes and computes the aggregation function for grouping variable 0. 
    Example: group_variable_fs: {0: [('0_max_quant', 'max', 'quant')]}.
    """

    group_attr = "(" + ", ".join(["key_" +
                                  group_attr for group_attr in V]) + ")"
    print(f"group_variable_fs with first scan: {aggregate_set}")

    if 0 in aggregate_set.keys():
        gv0 = [(f[0], f[1], f[2])for f in aggregate_set[0]]
        for f in gv0:
            if "avg" in f[1]:
                structure += ((" " * space) + "count_" +
                              f[0] + "= collections.defaultdict(int)\n")
                break
    structure += ((" " * space) + "for row in rows:\n")
    space += 2

    """Extracting grouping attributes such as 'cust' and 'prod'."""
    for attr in V:
        structure += ((" " * space) + "key_" + attr +
                      " = row[" + schema[attr][0] + "]\n")

    """Extract aggregated attributes (ex: quant)"""
    if 0 in aggregate_set.keys():
        fun_attr_set = set(f[2] for f in gv0)
        for attr in fun_attr_set:
            structure += ((" " * space) + attr +
                          " = row[" + schema[attr][0] + "]\n")

    """Wrtie first scan in the script"""
    group_key = "group[" + group_attr + "]"
    structure += ((" " * space) + "if not " + "(" +
                  " and ".join([group_key + "[\"" + attr + "\"]" for attr in V]) + "):\n")
    space += 2
    for v in V:
        structure += ((" " * space) + group_key +
                      '["' + v + '"]' + " = key_" + v + "\n")
    space -= 2

    """
    Writing the aggregation function into the script.    
    """
    if 0 in aggregate_set.keys():
        for f in gv0:
            if f[1] == "avg":
                structure += avgStructure(group_attr, f[0],
                                          "0", space, None)
            elif f[1] == "max":
                structure += maxStructure(group_attr, f[0],
                                          None, None, space, None)
            elif f[1] == "min":
                structure += minStructure(group_attr,
                                          f[0], None, None, space, None)
            elif f[1] == "count":
                structure += countStructure(group_attr, f[0], space, None)
            elif f[1] == "sum":
                structure += sumStructure(group_attr, f[0], space, None)

    return structure

def GVScan(S, V, C, G, schema, max_aggregate, min_aggregate, structure, space, aggregate_set, index):

    key_V = [f"key_{group_attr}" for group_attr in V]
    group_attr = "(" + ", ".join(key_V) + ")"
    process_attr = processAttr1(S, C, G)

    if not aggregate_set:
        group_variables_to_be_scan = {}
        aggregate_set = {}
    else:
        group_variables_to_be_scan = {
            index: [value[0] for value in aggregate_set]}
    for i, condition in enumerate(C):
        if group_variables_to_be_scan.get(i + 1):
            group_variables_to_be_scan[i +
                                       1] = group_variables_to_be_scan[i + 1] + [condition]
    """
    {0: [('0_max_quant', 'max', 'quant')], 1: [('1_avg_quant', 'avg', 'quant')], 2: [('2_avg_quant', 'avg', 'quant')], 3: [('3_avg_quant', 'avg', 'quant')]}
    Construct a dictionary to represent group variables for the scan.
    """
    structure += (" " * space) + f"# {index+1} scan\n"
    for value in aggregate_set:
        if "avg" in value[1]:
            structure += (" " * space) + \
                f"count_{value[0]} = collections.defaultdict(int)\n"
            
    structure += (" " * space) + f"for {group_attr} in group:\n"
    space += 2
    structure += (" " * space) + "for row in rows:\n"
    space += 2
    for attr in schema:
        structure += (" " * space) + f"{attr} = row[{schema[attr][0]}]\n"
    output_data = {}

    # S
    """
    This loop processes group variables specified in the select statement, for example, select 1.state, 1.quant
    """
    for attr in process_attr:
        for index, value in attr.items():
            output_data[index] = {'value': value, 'condition': processSuchthat(
                C[index-1], group_attr) if C[index-1] else []}
            output_data[index]['value'] = [
                f"{index}.{attr}" for attr in output_data[index]['value']]
            structure += f"{' ' * space}if {output_data[index]['condition']}:\n"
            space += 2
            for value in output_data[index]['value']:
                structure += f'{" " * space}group[{group_attr}]["{value}"] = {value.split(".")[1]} \n'
            space -= 2

    # F
    """
    This loop handles group variables defined in the Aggregate function statement, such as 0_avg_quant and 1_avg_quant.
    """
    for index, values in group_variables_to_be_scan.items():
        for value in values[:-1]:
            agg = value.split("_")
            condition = processSuchthat(C[index-1], group_attr)
            if not agg[1]:
                structure += noAggregate(
                    group_attr, agg[2], space, condition)
            else:
                if agg[1] == "avg":
                    structure += avgStructure(group_attr, value, str(index),
                                              space, condition) + f"\n"
                elif agg[1] == "max":
                    structure += maxStructure(
                        group_attr, value, max_aggregate[index], index, space, condition)
                elif agg[1] == "min":
                    structure += minStructure(
                        group_attr, value, min_aggregate[index], index, space, condition)
                elif agg[1] == "count":
                    structure += countStructure(group_attr,
                                                value, space, condition) + f"\n"
                elif agg[1] == "sum":
                    structure += sumStructure(group_attr,
                                              value, space, condition) + f"\n"

    return structure


def writeProject(S, G, script, space):
    my_string = ','.join(f"'{item}'" for item in S)
    output = ""
    output += ((" " * space) + "x = PrettyTable()\n")
    output += ((" " * space) + f"x.field_names = [" + my_string + "]\n")
    output += ((" " * space) + "for val in group.values():\n")
    space += 2
    if len(G) and len(G[0]):
        having = processHaving(G[0])
        output += ((" " * space) + "if " + having + ":\n")
        space += 2
    output += ((" " * space) + "row_str=''\n")
    output += ((" " * space) + "for key in val:\n")
    space += 2
    output += ((" " * space) + "if key in x.field_names:\n")
    space += 2
    # Check if key contains 'avg' and if so, round the value to two decimal places
    output += ((" " * space) + "if 'avg' in key and isinstance(val[key], (int, float)):\n")
    space += 2
    output += ((" " * space) + "row_str += str(round(val[key], 2)) + ','\n")
    space -= 2
    output += ((" " * space) + "else:\n")
    space += 2
    output += ((" " * space) + "row_str += str(val[key]) + ','\n")
    space -= 6
    output += ((" " * space) + "row_str = row_str[:-1]\n")
    output += ((" " * space) + "x.add_row(row_str.split(','))\n")
    space -= 2
    if len(G) and len(G[0]):
        space -= 2
    output += ((" " * space) + "print(x)\n")
    script += output
    return script
