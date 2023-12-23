# might need to chang the variable name
import psycopg2
import collections
import pathlib
from OutputProcess.OutputProcessor import *
from InputProcess.InputParser import *
from coreProcess.GV_process import *
from coreProcess.mf_Structure import *

template_path = str(pathlib.Path(__file__).parent.resolve())

def connect(file_name):
    space = 4
    template = open(template_path + '/Template/header.txt', mode='r')
    script = template.read() + "\n"
    template.close()
    table_name = "sales"
    conn = psycopg2.connect(
        host="localhost",
        database="sales",
        user="postgres",
        password="password",
        port="5432",
    )
    cursor = conn.cursor()

    with open(f"./Test Text/{file_name}.txt", "r") as my_file:
        file = my_file.read()
    input = input_parser(file)
    schema = {'cust': '0', 'prod': '1', 'day': '2', 'month': '3',
              'year': '4', 'state': '5', 'quant': '6', "date": '7'}
    S = input["SELECT ATTRIBUTE(S):"]
    N = input["NUMBER OF GROUPING VARIABLES(n):"]
    V = input["GROUPING ATTRIBUTES(V):"]
    F = input["F-VECT([F]):"]
    C = input["SELECT CONDITION-VECT([σ]):"]
    G = input["HAVING_CONDITION(G):"]
    mf = mf_Structure(S, F, G)
    script += outputQueryTable(table_name, space)
    script += outputMFStructure(mf, space)
    aggregate_set = processAgg(F)
    group_variable_attrs, max_aggregate, min_aggregate = processAttr1(
        S, C, G)
    print(f"group_variable_min:{min_aggregate}")
    script += ("\n" + (" " * space) + "## 1th Scan:\n")
    script = firstScan(V, schema, script, space, aggregate_set)
    script += ("\n" + (" " * space) + "## GV Scan:\n")
    for i in range(1,int(N[0])+1):
        print(aggregate_set)
        print(set)
        script = GVScan(S, V, C, G, schema, max_aggregate,min_aggregate, script, space, aggregate_set.get(i), i)
    script = writeProject(S, G, script, space)
    print(script)

    
    template_footer = open(template_path + '/Template/footer.txt', mode='r')
    script += template_footer.read() + "\n"
    template.close()
    file = open('query.py', mode='w')
    file.write(script)
    file.close()
    cursor.close()


if __name__ == '__main__':
    file_name = input("Please enter a file name in test text file:")
    connect(file_name)
