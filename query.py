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
    mf_structure = {'cust': [], '1_avg_quant': [], '2_avg_quant': [], '3_avg_quant': []}
    group = collections.defaultdict(lambda: dict(mf_structure))

    ## 1th Scan:
    for row in rows:
      key_cust = row[0]
      if not (group[(key_cust)]["cust"]):
        group[(key_cust)]["cust"] = key_cust

    ## GV Scan:
    count_1_quant = collections.defaultdict(int)
    for (key_cust) in group:
      for row in rows:
        cust = row[0]
        prod = row[1]
        day = row[2]
        month = row[3]
        year = row[4]
        state = row[5]
        quant = row[6]
        date = row[7]
        if cust==group[(key_cust)]["cust"] and state=="NY":
          if not group[(key_cust)]['1_avg_quant']:
            group[(key_cust)]['1_avg_quant'] = 1_avg_quant
            count_1_1_avg_quant[(key_cust)] += 1
          else:
            count_1_1_avg_quant[(key_cust)] += 1
            group[(key_cust)]['1_avg_quant'] += ((1_avg_quant - group[(key_cust)]['1_avg_quant'])/count_1_1_avg_quant[(key_cust)])

    count_2_quant = collections.defaultdict(int)
    for (key_cust) in group:
      for row in rows:
        cust = row[0]
        prod = row[1]
        day = row[2]
        month = row[3]
        year = row[4]
        state = row[5]
        quant = row[6]
        date = row[7]
        if cust==group[(key_cust)]["cust"] and state=="NJ":
          if not group[(key_cust)]['2_avg_quant']:
            group[(key_cust)]['2_avg_quant'] = 2_avg_quant
            count_2_2_avg_quant[(key_cust)] += 1
          else:
            count_2_2_avg_quant[(key_cust)] += 1
            group[(key_cust)]['2_avg_quant'] += ((2_avg_quant - group[(key_cust)]['2_avg_quant'])/count_2_2_avg_quant[(key_cust)])

    count_3_quant = collections.defaultdict(int)
    for (key_cust) in group:
      for row in rows:
        cust = row[0]
        prod = row[1]
        day = row[2]
        month = row[3]
        year = row[4]
        state = row[5]
        quant = row[6]
        date = row[7]
        if cust==group[(key_cust)]["cust"] and state=="CT":
          if not group[(key_cust)]['3_avg_quant']:
            group[(key_cust)]['3_avg_quant'] = 3_avg_quant
            count_3_3_avg_quant[(key_cust)] += 1
          else:
            count_3_3_avg_quant[(key_cust)] += 1
            group[(key_cust)]['3_avg_quant'] += ((3_avg_quant - group[(key_cust)]['3_avg_quant'])/count_3_3_avg_quant[(key_cust)])

    x = PrettyTable()
    x.field_names = ['cust','1_avg_quant','2_avg_quant','3_avg_quant']
    for val in group.values():
      row_str=''
      for key in val:
        if key in x.field_names:
          row_str+=str(val[key])+','
      row_str = row_str[:-1]
      x.add_row(row_str.split(','))
    print(x)
if __name__ == "__main__":
  query()
