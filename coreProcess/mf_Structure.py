def mf_Structure(S,F,G):
    mf_structure={}
    for s in S:
        type = getType(s)
        if s not in mf_structure:
            mf_structure[s]=[type,[]]
    for f in F:
        type = getType(f)
        if f not in mf_structure:
            mf_structure[f]=[type,[]]
    if (G) and (G[0]):
        array=G[0].split()
        for name in array:
            if "." in name or "_" in name:
                type = getType(name)
                if s not in mf_structure:
                    mf_structure[name]=[type,[]]
    return mf_structure
def getType(name):
    map = { 
    'cust': "str",
    'prod': "str",
    'day': "int",
    'month': "int",
    'year': "int",
    'quant': "int",
    'state': "str",
    "date":"date"
    }
    type=name
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
    # return what the mapping type
    return map.get(type)
    
