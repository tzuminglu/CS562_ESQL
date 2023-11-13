import collections
def processAgg(F):
    aggregate={}
    for f in F:
        array=f.split("_")
        key = int(array[0])
        if key not in aggregate:
            aggregate[key] = []
        aggregate[key].append((f,array[1], array[2]))
    return aggregate
def processSuchthat(conditions,groupby_attributes):
    processed = []
    array = conditions.split("and")
    operators = ["==", "<=", ">=", "<", ">", "!="]
    for condition in array:
        operator = next((op for op in operators if op in condition), "!=")
        splited = condition.split(operator)
        left = splited[0].split(".")[1]
        right = splited[1]
        left=left.strip()
        right=right.strip()
        if "date" in left:
            right ='date.fromisoformat("'+right+'")'
            processed.append(left+operator+right)
        elif "'" in right or right.isdigit():
            processed.append(left+operator+right)
        else:
            right ='group['+groupby_attributes+']["'+right+'"]'
            processed.append(left+operator+right)
    return processed
def processHaving(havings):
    processed = []
    array = havings.split("and")
    operators = ["==", "<=", ">=", "<", ">", "!="]
    for having in array:
        operator = next((op for op in operators if op in having), "!=")
        splited = having.split(operator)
        left = splited[0].split()
        right = splited[1].split()
        left = ['val["'+l+'"]' if "." in l or "_" in l else l for l in left]
        right = ['val["'+r+'"]' if "." in r or "_" in r else r for r in right]
        L_string = ' '.join(left)
        R_string = ' '.join(right)
        L_string=L_string.strip()
        R_string=R_string.strip()
        processed.append(L_string+operator+R_string)
    return processed
def processAttr1(S, C, G):
    attrs = {}
    operators = ["==", "<=", ">=", "<", ">", "!="]
    group_variable_attrs = {}
    group_variable_attrs_max_aggregate = {}
    group_variable_attrs_min_aggregate = {}
    
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
                    group_variable_attrs[number] = attrs.get(number, [])
    
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
                        group_variable_attrs_max_aggregate[number] = attrs.get(number, [])
                        group_variable_attrs[number] = attrs.get(number, [])
                    if "min" in right:
                        group_variable_attrs_min_aggregate[number] = attrs.get(number, [])
                        group_variable_attrs[number] = attrs.get(number, [])
    
    return group_variable_attrs, group_variable_attrs_max_aggregate, group_variable_attrs_min_aggregate








