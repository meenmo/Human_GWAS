import pandas as pd
import pyodbc

sql_conn =  pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=PARKSLAB;DATABASE=Human_GWAS;Trusted_Connection=Yes')


query = "SELECT TOP 100 [chr],[bp],[beta],[p_value],[rsid],[trait],[table_name] FROM [Human_GWAS].[dbo].[BMI_giant_bmi]"

df = pd.read_sql(query, sql_conn)

print(df)
