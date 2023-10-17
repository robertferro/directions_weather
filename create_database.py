import duckdb


con = duckdb.connect(database='analytics.db') 

with open('init.sql', 'r') as sql_file:
    sql_script = sql_file.read()

sql_statements = sql_script.split(';')

sql_statements = [sql.strip() for sql in sql_statements]

for sql in sql_statements:
    if sql:
        con.execute(sql)
        
con.close()