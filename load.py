import pandas as pd
import pyodbc

#Connect to SQL Server
sql_conn =  pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=PARKSLAB;DATABASE=Human_GWAS;Trusted_Connection=Yes')

#Load Tables from SQL Server into Pandas DataFrame
hg19            = pd.read_sql("SELECT * FROM hg19", sql_conn)
giant           = pd.read_sql("SELECT TOP 500 * FROM BMI_giant_bmi", sql_conn)
japanese        = pd.read_sql("SELECT TOP 500 * FROM BMI_japanese_bmi", sql_conn)
ukbb_bmi        = pd.read_sql("SELECT TOP 500 * FROM BMI_ukbb_bmi_Neale", sql_conn)
surakka         = pd.read_sql("SELECT TOP 500 * FROM Lipid_Engage_Surakka_NG", sql_conn)
east_asian      = pd.read_sql("SELECT TOP 500 * FROM Lipid_Exome_Lu_East_Asian_NG", sql_conn)
european        = pd.read_sql("SELECT TOP 500 * FROM Lipid_Exome_Lu_European_and_East_Asian_NG", sql_conn)
exome           = pd.read_sql("SELECT TOP 500 * FROM Lipid_GLGC_Exome_Liu_NG", sql_conn)
glgc            = pd.read_sql("SELECT TOP 500 * FROM Lipid_GLGC_Willer_NG", sql_conn)
lipid_japanese  = pd.read_sql("SELECT TOP 500 * FROM Lipid_Japanese_lipid_trait_Kanai_NG", sql_conn)
lipid_mvp       = pd.read_sql("SELECT TOP 500 * FROM Lipid_MVP_Klarin_NG", sql_conn)
lipid_spracklen = pd.read_sql("SELECT TOP 500 * FROM Lipid_Spracklen_Hum_Mol_Genetics", sql_conn)
high_chol       = pd.read_sql("SELECT TOP 500 * FROM Lipid_UKBB_high_cholesterol_ukbb_Connor_alkesgroup", sql_conn)
ukbb_lipid      = pd.read_sql("SELECT TOP 500 * FROM Lipid_UKBB_lipid_trait_Neale", sql_conn)
ukbb_statin     = pd.read_sql("SELECT TOP 500 * FROM Lipid_UKBB_statin_usage_Neale", sql_conn)

#Makes all gene names into lower cases since SQL is not case-sensitive, but Python is.
hg19['gene_name'] = hg19['gene_name'].str.lower()


table_list = [hg19, giant,japanese,ukbb_bmi,surakka,east_asian,european,exome,glgc,lipid_japanese,lipid_mvp,lipid_spracklen,high_chol,ukbb_lipid,ukbb_statin]
table_name = ["hg19","giant","japanese","ukbb_bmi","surakka","east_asian","european","exome","glgc","lipid_japanese","lipid_mvp","lipid_spracklen","high_chol","ukbb_lipid","ukbb_statin"]

#Add a column named 'table_name' whose values are corresponding table name
c=0
for table in table_list:
    table['table_name'] = table_name[c]
    c+=1


print(max(hg19.loc[(hg19['gene_name']=='samd11')]['chr_start']))
#& (hg19['chr']=='1')
