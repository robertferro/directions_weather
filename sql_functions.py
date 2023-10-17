import duckdb

def retrying_data(table):
    con = duckdb.connect(database='analytics.db') 
    consulta = f"SELECT * FROM DIRECTIONS_WEATHER.{table}"
    resultado = con.execute(consulta)
    con.close()
    return resultado

def insert_data(df,table):
    con = duckdb.connect(database='analytics.db') 
    con.register('dados', df)
    con.execute(f"INSERT INTO DIRECTIONS_WEATHER.{table} SELECT * FROM dados;")
    con.close()