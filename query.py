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
    mf_structure = {'prod': None, 'month': None, '1_avg_quant': None, '2_avg_quant': None}
    group = collections.defaultdict(lambda: dict(mf_structure))

    ## 1th Scan:
    for row in rows:
      key_prod = row[1]
      key_month = row[3]
      if not (group[(key_prod, key_month)]["prod"] and group[(key_prod, key_month)]["month"]):
        group[(key_prod, key_month)]["prod"] = key_prod
        group[(key_prod, key_month)]["month"] = key_month

    ## GV Scan:
    # 2 scan
    count_1_avg_quant = collections.defaultdict(int)
    for (key_prod, key_month) in group:
      for row in rows:
        cust = row[0]
        prod = row[1]
        day = row[2]
        month = row[3]
        year = row[4]
        state = row[5]
        quant = row[6]
        date = row[7]
        if prod==group[(key_prod, key_month)]["prod"] and month<group[(key_prod, key_month)]["month"]:
          if not group[(key_prod, key_month)]['1_avg_quant']:
            group[(key_prod, key_month)]['1_avg_quant'] = quant
            count_1_avg_quant[(key_prod, key_month)] += 1
          else:
            count_1_avg_quant[(key_prod, key_month)] += 1
            group[(key_prod, key_month)]['1_avg_quant'] += ((quant - group[(key_prod, key_month)]['1_avg_quant'])/count_1_avg_quant[(key_prod, key_month)])

    # 3 scan
    count_2_avg_quant = collections.defaultdict(int)
    for (key_prod, key_month) in group:
      for row in rows:
        cust = row[0]
        prod = row[1]
        day = row[2]
        month = row[3]
        year = row[4]
        state = row[5]
        quant = row[6]
        date = row[7]
        if prod==group[(key_prod, key_month)]["prod"] and month>group[(key_prod, key_month)]["month"]:
          if not group[(key_prod, key_month)]['2_avg_quant']:
            group[(key_prod, key_month)]['2_avg_quant'] = quant
            count_2_avg_quant[(key_prod, key_month)] += 1
          else:
            count_2_avg_quant[(key_prod, key_month)] += 1
            group[(key_prod, key_month)]['2_avg_quant'] += ((quant - group[(key_prod, key_month)]['2_avg_quant'])/count_2_avg_quant[(key_prod, key_month)])

    x = PrettyTable()
    x.field_names = ['prod','month','1_avg_quant','2_avg_quant']
    for val in group.values():
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
