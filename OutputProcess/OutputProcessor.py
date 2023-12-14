from AggregationProcessor import *
import sys
sys.path.append('../')
from coreProcess.GV_process import *



# this function is to fecth data from the query table


def outputQueryTable(table_name, indentation):
    output = ("\n" + (" " * indentation) +
              f"query = 'select * from {table_name}'\n")
    output += ((" " * indentation) + "cursor.execute(query)\n")
    output += ((" " * indentation) + "rows = cursor.fetchall()\n")
    return output


def outputMFStructure(structure, type, indentation):
    output = ((" " * indentation) + "mf_structure = ")
    output += (str(structure) + "\n")
    output += ((" " * indentation) + "mf_type = ")
    output += (str(type) + "\n")
    output += ((" " * indentation) +
               "group = collections.defaultdict(lambda: dict(mf_structure))\n")

    return output


def firstScan(V, schema, structure, indentation, group_variable_fs):
    """The function to write the script of first initial scan"""

    # the function writes the script of the first scan, the first scan fill grouping attribute into the hashmap
    # and process the aggregation function of the grouping variable 0
    # group_variable_fs: {0: [('0_max_quant', 'max', 'quant')]}

    group_attr = "(" + ", ".join(["key_" +
                                  group_attr for group_attr in V]) + ")"
    gv0 = [(f[0], f[1], f[2])for f in group_variable_fs[0]]
    print(group_variable_fs)
    for f in gv0:
        if "avg" in f[1]:
            structure += ((" " * indentation) + "count_0_" +
                          f[2] + "= collections.defaultdict(int)\n")
    structure += ((" " * indentation) + "for row in rows:\n")
    indentation += 2

    # extract grouping attributes (ex: cust, prod)
    for attr in V:
        structure += ((" " * indentation) + "key_" + attr +
                      " = row[" + schema[attr][0] + "]\n")

    # extract aggregated attributes (ex: quant)
    fun_attr_set = set(f[2] for f in gv0)
    for attr in fun_attr_set:
        structure += ((" " * indentation) + attr +
                      " = row[" + schema[attr][0] + "]\n")

    # first filling the grouping attributes, this process only works in first scan
    group_key = "group[" + group_attr + "]"
    structure += ((" " * indentation) + "if not " +
                  " and ".join([group_key + "[\"" + attr + "\"]" for attr in V]) + "\n")
    indentation += 2
    for v in V:
        structure += ((" " * indentation) + group_key +
                      '["' + v + '"]' + " = key_" + v + "\n")
    indentation -= 2

    for f in gv0:
        if f[1] == "avg":
            structure += avgStructure(group_attr, f, "0", indentation, None)
        elif f[1] == "max":
            structure += maxStructure(group_attr, f, None, indentation, None)
        elif f[1] == "min":
            structure += minStructure(group_attr, f, None, indentation, None)
        elif f[1] == "count":
            structure += countStructure(group_attr, f, indentation, None)
        elif f[1] == "sum":
            structure += sumStructure(group_attr, f, indentation, None)

    return structure


# print(firstScan(['cust', 'prod'], {'cust': ['0', 'character varying'], 'prod': ['1', 'character varying'], 'day': ['2', 'integer'], 'month': [
#     '3', 'integer'], 'year': ['4', 'integer'], 'state': ['5', 'character'], 'quant': ['6', 'integer'], 'date': ['7', 'date']}, "", 0, {0: [('0_max_quant', 'max', 'quant')], 1: [('1_avg_quant', 'avg', 'quant')], 2: [('2_avg_quant', 'avg', 'quant')], 3: [('3_avg_quant', 'avg', 'quant')]}))


def GVScan(S, V, C, G, schema, max_aggregate_attrs, min_aggregate_attrs, structure, indentation, group_variable_fs):

    key_V = [f"key_{group_attr}" for group_attr in V]
    group_attr = "(" + ", ".join(key_V) + ")"
    print(f'group_variable_fs: {group_variable_fs}')
    print(f'group_attr: {group_attr}')
    process_attr = processAttr1(S, C, G)
    print(f"process_attr: {processAttr1(S, C, G)}")
    group_variables_to_be_scan = {
        index: value[0] for index, value in group_variable_fs.items() if index != 0}
    print(group_variables_to_be_scan)
    for index, condition in enumerate(C):
        if group_variables_to_be_scan.get(index + 1):
            group_variables_to_be_scan[index + 1] = group_variables_to_be_scan[index + 1] + (C[index],)
        print(f"index: {index} condition: {condition}")
    # processed_condition = processSuchthat(C[0], group_attr)
    # print(f"\nprocessed_condition: {processed_condition}")
    print(f"\ngroup_variables_to_be_scan: {group_variables_to_be_scan}")

    # {0: [('0_max_quant', 'max', 'quant')], 1: [('1_avg_quant', 'avg', 'quant')], 2: [('2_avg_quant', 'avg', 'quant')], 3: [('3_avg_quant', 'avg', 'quant')]}

    # for group_variable in next_scan:
    for index, value in group_variables_to_be_scan.items():
        # print(f'\n{index, value}')
        if "avg" in value[1]:
            structure += (" " * indentation) + \
                f"count_{index}_{value[2]} = collections.defaultdict(int)\n"


    structure += (" " * indentation) + f"for {group_attr} in group:\n"
    indentation += 2
    structure += (" " * indentation) + "for row in rows:\n"
    indentation += 2
    for attr in schema:
            structure += (" " * indentation) + f"{attr} = row[{schema[attr][0]}]\n"

    output_data = {}
    for attr in process_attr:
        for index, value in attr.items():
            output_data[index] = {'value': value, 'condition': processSuchthat(C[index-1], group_attr) if C[index-1] else []}
            output_data[index]['value'] = [f"{index}.{attr}" for attr in output_data[index]['value']]
            # structure += noAggregate(group_attr, output_data[index].value, indentation, output_data[index].condition)
            print(output_data[index])
            structure += f"{' ' * indentation}if {output_data[index]['condition']}:\n"
            indentation += 2
            for value in output_data[index]['value']:
                structure += f'{" " * indentation}group[({group_attr})][{value}] = {value.split(".")[1]} \n'
            indentation -= 2
    print(output_data)


    for index, value in group_variables_to_be_scan.items():

        print(f"index: {index}, value: {value}")
        condition = processSuchthat(value[3], group_attr)
        if not value[1]:
            structure += noAggregate(
                group_attr, value[1], indentation, condition)
        else:
            if value[1] == "avg":
                structure += avgStructure(group_attr, value, str(index),
                                          indentation, condition) + f"\n"
            elif value[1] == "max":
                structure += maxStructure(
                    group_attr, value, max_aggregate_attrs[index], indentation, condition)
            elif value[1] == "min":
                structure += minStructure(
                    group_attr, value, min_aggregate_attrs[index], indentation, condition)
            elif value[1] == "count":
                structure += countStructure(group_attr,
                                            value, indentation, condition) + f"\n"
            elif value[1] == "sum":
                structure += sumStructure(group_attr,
                                          value, indentation, condition) + f"\n"

    return structure
# print(firstScan(['cust', 'prod'],
#     {'cust': ['0', 'character varying'], 'prod': ['1', 'character varying'], 'day': ['2', 'integer'], 'month': ['3', 'integer'], 'year': ['4', 'integer'], 'state': ['5', 'character'], 'quant': ['6', 'integer'], 'date': ['7', 'date']},
#     "",
#     0,
#     {0: [('0_max_quant', 'max', 'quant')], 1: [('1_avg_quant', 'avg', 'quant')], 2: [('2_avg_quant', 'avg', 'quant')], 3: [('3_avg_quant', 'avg', 'quant')]}))

# print(f"Script 5")
# print(GVScan(['cust', '1_avg_quant', '2_avg_quant', '3_avg_quant'],
#              ['cust'],
#              ['1.cust == cust and 1.state == "NY"', '2.cust == cust and 2.state == "NJ"',
#                  '3.cust == cust and 3.state == "CT"'],
#              [''],
#              {'cust': ['0', 'character varying'], 'prod': ['1', 'character varying'], 'day': ['2', 'integer'], 'month': [
#                  '3', 'integer'], 'year': ['4', 'integer'], 'state': ['5', 'character'], 'quant': ['6', 'integer'], 'date': ['7', 'date']},
#                  None,
#              "",
#              2,
#              {1: [('1_avg_quant', 'avg', 'quant')], 2: [
#                  ('2_avg_quant', 'avg', 'quant')], 3: [('3_avg_quant', 'avg', 'quant')]}
#              ))

print("\nScript 2")
print(GVScan(['cust', 'prod', '1.quant', '1.state', '1.date'],
              ['cust', 'prod'],
             ['1.cust == cust and 1.prod == prod and 1.quant == 0_max_quant'],
             [''],
             {'cust': ['0', 'character varying'], 'prod': ['1', 'character varying'], 'day': ['2', 'integer'], 'month': [
                 '3', 'integer'], 'year': ['4', 'integer'], 'state': ['5', 'character'], 'quant': ['6', 'integer'], 'date': ['7', 'date']},
             None,
             None,
             "",
             2,
             {0: [('0_max_quant', 'max', 'quant')]}
             ))

# print(GVScan(['cust', 'prod', '0_avg_quant', '1_avg_quant', '2_avg_quant'],
#              ['cust', 'prod'],
#              ['1.cust == cust and 1.prod == prod and 1.year == 2018 and 1.quant > 0_avg_quant', '2.cust == cust and 2.prod == prod and 2.year == 2019 and 2.quant > 1_avg_quant'],
#              [''],
#              {'cust': ['0', 'character varying'], 'prod': ['1', 'character varying'], 'day': ['2', 'integer'], 'month': [
#                  '3', 'integer'], 'year': ['4', 'integer'], 'state': ['5', 'character'], 'quant': ['6', 'integer'], 'date': ['7', 'date']},
#             None,
#             "",
#             2,
#             {0: [('0_avg_quant', 'avg', 'quant')], 1: [('1_avg_quant', 'avg', 'quant')], 2: [('2_avg_quant', 'avg', 'quant')]}
#              ))]

print("Script 3\n")
print(GVScan(['cust', 'prod', '1.quant', '1.state', '1.date'],
             ['cust', 'prod'],
             ['1.cust == cust and 1.prod == prod and 1.date > 2019-05-31 and 1.date < 2019-09-01'],
             ['1_sum_quant * 10 > 0_sum_quant and 1.quant == 1_min_quant and 1_min_quant > 150'],
             {'cust': ['0', 'character varying'], 'prod': ['1', 'character varying'], 'day': ['2', 'integer'], 'month': [
                 '3', 'integer'], 'year': ['4', 'integer'], 'state': ['5', 'character'], 'quant': ['6', 'integer'], 'date': ['7', 'date']},
            None,
            {1: ['1.quant', '1.state', '1.date']},
            "",
            2,
            {0: [('0_sum_quant', 'sum', 'quant')], 1: [('1_min_quant', 'min', 'quant'), ('1_sum_quant', 'sum', 'quant')]}
             ))