from cross_ref_lipid_gwas import *

for i in range (1,16):
    sql_conn =  pyodbc.connect("""
                               DRIVER={ODBC Driver 11 for SQL Server};
                               SERVER=PARKSLAB;
                               DATABASE=Human_GWAS;
                               Trusted_Connection=Yes;
                               """)
    chosen_table = i
    gene_name = "sesn1"
    margin  = 200000
    cutoff  = 1
    hg19 = get_hg19(sql_conn, gene_name, margin)
    df = get_df(sql_conn, hg19, chosen_table, margin, cutoff)
    print(df.to_string())
    save_option(df,sql_conn)