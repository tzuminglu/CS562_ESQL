import psycopg2
import collections
from datetime import date, datetime
import string
from prettytable import PrettyTable

def query():
    conn = psycopg2.connect(
        host="localhost",
        database="sales",
        user="postgres",
        password="password",
        port="5432",
    )
    cursor = conn.cursor()

    query = 'select * from sales'
    cursor.execute(query)
    rows = cursor.fetchall()
    mf_structure = {'cust': None, 'prod': None, '1.quant': None, '1.date': None, '0_max_quant': None}
    group = collections.defaultdict(lambda: dict(mf_structure))

    ## 1th Scan:
    for row in rows:
      key_cust = row[0]
      key_prod = row[1]
      quant = row[6]
      if not (group[(key_cust, key_prod)]["cust"] and group[(key_cust, key_prod)]["prod"]):
        group[(key_cust, key_prod)]["cust"] = key_cust
        group[(key_cust, key_prod)]["prod"] = key_prod
      if not group[(key_cust, key_prod)]["0_max_quant"]:
        group[(key_cust, key_prod)]["0_max_quant"] = quant
      else:
        if quant > group[(key_cust, key_prod)]["0_max_quant"]:
          group[(key_cust, key_prod)]["0_max_quant"] = quant

    ## GV Scan:
    # 2 scan
    for (key_cust, key_prod) in group:
      for row in rows:
        cust = row[0]
        prod = row[1]
        day = row[2]
        month = row[3]
        year = row[4]
        state = row[5]
        quant = row[6]
        date = row[7]
        if cust==group[(key_cust, key_prod)]["cust"] and prod==group[(key_cust, key_prod)]["prod"] and quant==group[(key_cust, key_prod)]["0_max_quant"]:
          group[(key_cust, key_prod)]["1.quant"] = quant 
          group[(key_cust, key_prod)]["1.date"] = date 
    x = PrettyTable()
    x.field_names = ['cust','prod','1.quant','1.date']
    for val in group.values():
      if val["0_max_quant"]>=1000:
        row_str=''
        for key in val:
          if key in x.field_names:
            if 'avg' in key and isinstance(val[key], (int, float)):
              row_str += str(round(val[key], 2)) + ','
            else:
              row_str += str(val[key]) + ','
        row_str = row_str[:-1]
        x.add_row(row_str.split(','))
    print(x)
if __name__ == "__main__":
  query()
