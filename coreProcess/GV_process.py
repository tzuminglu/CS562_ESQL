import sys
import collections
import re


def processAgg(F):
    aggregate = {}
    for f in F:
        array = f.split("_")
        key = int(array[0])
        if key not in aggregate:
            aggregate[key] = []
        aggregate[key].append((f, array[1], array[2]))
    return aggregate
# convert SELECT CONDITION-VECT statment into conditions that can dirctly usued in aggreate process function
# ex
# GROUPING ATTRIBUTES(V):
# cust, prod
# SELECT CONDITION-VECT([]):
# change 1.cust == cust and 1.prod == prod and 1.quant == 0_max_quant
# into: group[cust,prod]==cust and group[cust,prod]==prod and group[cust,prod][0_max_quant] == quant


def processSuchthat(conditions, groupby_attributes):
    processed = []
    array = conditions.split("and")
    operators = ["==", "<=", ">=", "<", ">", "!="]
    for condition in array:
        operator = next((op for op in operators if op in condition), "!=")
        splited = condition.split(operator)
        left = splited[0].split(".")[1]
        right = splited[1]
        left = left.strip()
        right = right.strip()
        if "date" in left:
            right = 'date.fromisoformat("'+right+'")'
            processed.append(left+operator+right)
        elif '"' in right or right.isdigit():
            processed.append(left+operator+right)
        elif "'" in right or right.isdigit():
            processed.append(left+operator+right)
        else:
            right = 'group['+groupby_attributes+']["'+right+'"]'
            processed.append(left+operator+right)
    statement = ' and '.join(processed)
    return statement


def processHaving(havings):
    processed = []
    array = re.split('(and|or)', havings)
    operators = ["==", "<=", ">=", "<", ">", "!="]

    for having in array:
        # Skip if the element is 'and' or 'or'
        if having in ['and', 'or']:
            processed.append(having)
            continue

        # Identify and split by the operator in the expression
        operator = next((op for op in operators if op in having), "!=")
        splited = re.split('({})'.format(operator), having)
        left, right = splited[0].split(), splited[2].split()
        # Replace elements in left and right
        left = ['val["'+l+'"]' if "." in l or "_" in l else l for l in left]
        right = ['val["'+r+'"]' if "." in r or "_" in r else r for r in right]

        # Join the lists back into strings
        L_string, R_string = ' '.join(left).strip(), ' '.join(right).strip()

        # Reconstruct the expression with the operator
        processed_expression = L_string + operator + R_string
        processed.append(processed_expression)

    # Join the processed expressions with their original logical operators
    statement = ' '.join(processed)
    return statement


def processAttr1(S, C, G):
    attrs = {}
    operators = ["==", "<=", ">=", "<", ">", "!="]
    group_variable = {}
    max_aggregate = {}
    min_aggregate = {}

    for s in S:
        if "." in s:
            splited = s.split(".")
            number = int(splited[0])
            if number not in attrs:
                attrs[number] = []
            attrs[number].append(splited[1])

    for c in C:
        array = c.split(" and ")
        for a in array:
            operator = next((op for op in operators if op in a), None)
            if operator:
                statement = a.split(operator)
                number = int(statement[0].split(".")[0])
                right = statement[1]
                if "max" in right or "min" in right:
                    group_variable[number] = attrs.get(number, [])

    for g in G:
        array = g.split(" and ")
        for a in array:
            operator = next((op for op in operators if op in a), None)
            if operator:
                statement = a.split(operator)
                if "." in statement[0]:
                    number = int(statement[0].split(".")[0])
                    right = statement[1]
                    if "max" in right:
                        max_aggregate[number] = attrs.get(
                            number, [])
                        group_variable[number] = attrs.get(number, [])
                    if "min" in right:
                        min_aggregate[number] = attrs.get(
                            number, [])
                        group_variable[number] = attrs.get(number, [])

    return group_variable, max_aggregate, min_aggregate


# print(f"{processAgg(F)}\n")
# print(OutputParser.GVScan(S, V, C, G,  
#                           {'cust': ['0', 'character varying'], 'prod': ['1', 'character varying'], 'day': ['2', 'integer'], 'month': ['3', 'integer'], 'year': ['4', 'integer'], 'state': ['5', 'character'], 'quant': ['6', 'integer'], 'date': ['7', 'date']},
#                           None,
#                           "", 2, mf))
# example: mf =  processSuchthat("1.cust == cust and 1.prod == prod and 1.date > 2019-05-31 and 1.date < 2019-09-01","cust, prod"):
# example: mf = processHaving(G[0])
