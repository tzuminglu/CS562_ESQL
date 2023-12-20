def mf_Structure(S,F,G):
    mf_structure={}
    for s in S:
        if s not in mf_structure:
            mf_structure[s]=None
    for f in F:
        if f not in mf_structure:
            mf_structure[f]=None
    if (G) and (G[0]):
        array=G[0].split()
        for name in array:
            if "." in name or "_" in name:
                if s not in mf_structure:
                    mf_structure[name]=None
    print(f"md_structure: {mf_structure}")
    return mf_structure
    
