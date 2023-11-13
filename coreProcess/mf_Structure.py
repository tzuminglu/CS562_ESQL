def mf_Structure(S,F,G,table):
    mf_structure={}
    for s in S:
        type = getType(s,table)
        if s not in mf_structure:
            mf_structure[s]=[type,[]]
    for f in F:
        type = getType(f,table)
        if f not in mf_structure:
            mf_structure[f]=[type,[]]
    if (G) and (G[0]):
        array=G[0].split()
        for name in array:
            if "." in name or "_" in name:
                type = getType(name,table)
                if s not in mf_structure:
                    mf_structure[name]=[type,[]]
    return mf_structure
def getType(name,table):
    map = { 
    'character': "str",
    'character varying': "str",
    'integer': "int",
    'date': "date",
    'float': "float",
    }
    type=""
    # normal case like 1.cust, using split to get cust
    if "."in name:
        type=name.split(".")[1]
    # aggregation function case like 1_avg_cust, using split to get avg if not get cust 
    elif "_" in name:
        array = name.split("_")
        if array[1]=="count":
            return "int"
        elif array[1]=="avg":
            return "float"
        else:
            type=array[2]
    return map[table[type][1]]

    
