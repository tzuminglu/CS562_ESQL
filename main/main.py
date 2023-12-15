import psycopg2
import collections
import pathlib
from Config.config import config
from coreProcess.mf_Structure import *
from coreProcess.GV_process import *
from CoreProcess.schemaProcess import * # might need to chang the variable name
from InputProcess.InputParser import *
from OutputProcess.outputProcess import * # might need to chang the variable name

template_path = str(pathlib.Path(__file__).parent.resolve())
def connect():
    space = 4
    template = open(template_path + '/Template/template_header.txt',mode='r')
    script = template.read() + "\n"
    template.close()
    table_name = "sales"
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="xxxxxx" #need to change the variable name
    )
    cursor = conn.cursor()
    file = None
    with open(r"C:\Users\asd19\Desktop\CS562_ESQL\main\query_input1.txt") as my_file:
        file = my_file.read()
    input=input_parser(file)
    schema = {'cust': '0','prod': '1','day': '2','month': '3','year':'4','state': '5','quant': '6',"date":'7'}
    S = input["SELECT ATTRIBUTE(S):"]
    N = input["NUMBER OF GROUPING VARIABLES(n):"]
    V = input["GROUPING ATTRIBUTES(V):"]
    F = input["F-VECT([F]):"]
    C = input["SELECT CONDITION-VECT([]):"]
    G = input["HAVING_CONDITION(G):"]
    mf= mf_structure(S, F, G)
    script += writeQueryTable(table_name,space)
    script += writeMFStructure(mf,space)
    aggregate_set = processAgg(F)

    script += ("\n" + (" " * space) + "1th Scan:\n")
    script = writeFirstScan(V, schema, script,space,aggregate_set)
    # do the main scan here
    #
    #
    #
    #----------------------
    script = writeProject(S, G, schema, script, space)
    template_footer = open(template_path + '/Template/template_footer.txt',mode='r')
    script += template_footer.read() + "\n"
    template.close()
    file = open('query.py',mode='w')
    file.write(script)
    file.close()
    cursor.close()


    if __name__ == '__main__':
        connect()