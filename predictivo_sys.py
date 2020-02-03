import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
import itertools
warnings.filterwarnings("ignore")

import cx_Oracle
con = cx_Oracle.Connection(user='usuario', password='password', dsn='RAC8.WORLD')

def predictive_system(canal_venta):
	
	query = """select trunc(fecha,'month') fecha,sum(nvl(volumen,0))/max(dias_laborables) volumen_avg
			   from jlcb_tmp 
			  where to_char(fecha,'yyyymm') < to_char(sysdate,'yyyymm')
                and canal_venta = '%s'
				and canal_venta <> 'CANAL NUEVO'
              group by trunc(fecha,'month')
		      order by 1""" %(canal_venta)

	df = pd.read_sql(query, con)

	df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d%b%Y')
	df = df.set_index('FECHA')
	dates = df.index
	Y = df.copy()

	p = d = q = range(0, 2)
	pdq = list(itertools.product(p, d, q))
	seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

	min = 99999999
	param = (0, 0, 0)
	param_aic = (0, 0, 0, 0)

	for param in pdq:
		for param_seasonal in seasonal_pdq:
			try:
				mod = sm.tsa.statespace.SARIMAX(Y,
												order=param,
												seasonal_order=param_seasonal,
												enforce_stationarity=False,
												enforce_invertibility=False)

				results = mod.fit()

				if results.aic < min:
					min=results.aic
					param_aic = param
					param_seasonal_aic = param_seasonal
				
				print(canal_venta) 
				print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
			except:
				continue
			
	print (param_aic)
	print (param_seasonal_aic)
			
	mod = sm.tsa.statespace.SARIMAX(Y,
									order=param_aic,
									seasonal_order=param_seasonal_aic,
									enforce_stationarity=False,
									enforce_invertibility=False)

	results = mod.fit()

	pred = results.get_prediction(start=pd.to_datetime('2019-05-01'), dynamic=False)
	pred_ci = pred.conf_int()
	pred_uc = results.get_forecast(steps=6)
	pred_ci = pred_uc.conf_int()

	predictions = mod.fit(disp=False).predict(steps=6)

	fcast1 = results.forecast(10)
	df_forecast = pd.Series.to_frame(fcast1)

	query_dias_laborables = """select trunc(fecha,'month') fecha,max(dias_laborables)
							     from jlcb_tmp
						     group by trunc(fecha,'month')
							 order by 1"""
	df_dias_laborables = pd.read_sql(query_dias_laborables, con)

	df_dias_laborables['FECHA'] = pd.to_datetime(df_dias_laborables['FECHA'], format='%d%b%Y')
	df_dias_laborables = df_dias_laborables.set_index('FECHA')

	df_end = df_forecast.merge(df_dias_laborables, left_index=True, right_index=True)

	print(df_end[0]*df_end['MAX(DIAS_LABORABLES)'])
	print('')
	print ('El canal seleccionado fue: ')
	print (canal_venta)
	
	return(df_end.index[0],df_end[0]*df_end['MAX(DIAS_LABORABLES)'])