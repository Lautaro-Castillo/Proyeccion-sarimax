import pandas as pd
import cx_Oracle
from predictivo_sys import predictive_system

con = cx_Oracle.Connection(user='usuario', password='password', dsn='RAC8.WORLD')

query = """select distinct canal_venta
			   from jlcb_tmp 
			  where to_char(fecha,'yyyymm') < to_char(sysdate,'yyyymm')
			    and canal_venta <> 'CANAL NUEVO'"""

df = pd.read_sql(query, con)

col_names =  ['FECHA','CANAL_VENTA','TOTAL']
df2  = pd.DataFrame(columns = col_names)

for i in (df.CANAL_VENTA):
	print(i)
	a,b = predictive_system(i)
	df2 = df2.append({'FECHA':[a],'CANAL_VENTA':[i], 'TOTAL':[b]},ignore_index=True)
	
print (df2)