# Proyeccion-sarimax

Se utiliza el archivo predictivo_sys_run.py para correr el modelo.
El mismo utiliza la función creada "predictive_system" del archivo predictivo_sys.py la cual recibe como parametro el canal de venta sobre el cual se va a realizar la iteración. El mismo es obtenido de una base de datos oracle y se itera la función por cada canal de venta ingresado, obteniendo asi proyecciones individuales para cada uno.
Tener en cuenta de que el modelo configura parametros de estacionalidad diferentes para cada Canal eligiendo la configuración con menor AIC posible.
