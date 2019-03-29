import pandas as pd
import pyodbc

while True:
    #Connect to SQL Server
    sql_conn =  pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=PARKSLAB;DATABASE=Human_GWAS;Trusted_Connection=Yes')

    choose_table = input("Which tables do you want to include?\n\n 1. BMI_giant_bmi\n 2. BMI_japanese_bmi \n 3. BMI_ukbb_bmi_Neale \n 4. Lipid_Engage_Surakka_NG \n 5. Lipid_Exome_Lu_East_Asian_NG \n 6. Lipid_Exome_Lu_European_and_East_Asian_NG \n 7. Lipid_GLGC_Willer_NG \n 8. Lipid_Japanese_lipid_trait_Kanai_NG \n 9. Lipid_MVP_Klarin_NG \n 10.Lipid_Spracklen_Hum_Mol_Genetics \n 11.Lipid_UKBB_high_cholesterol_ukbb_Connor_alkesgroup \n 12.Lipid_UKBB_lipid_trait_Neale \n 13.Lipid_UKBB_statin_usage_Neale\n\nChoose the options seperataed by comma. e.g.) 1,3,5\n")

    #Obtain index of chosen tables as a list
    chosen_list = [int(i) for i in choose_table.split(",")]

    for i in chosen_list:
        ct = 1
        if ct == i:
            #Load Tables from SQL Server into Pandas DataFrame
            hg19 = pd.read_sql("SELECT * FROM hg19", sql_conn)
            continue
        ct += 1

        if ct == i:
            giant = pd.read_sql("SELECT TOP 500 * FROM BMI_giant_bmi", sql_conn)
            continue
        ct += 1

        if ct == i:
            japanese = pd.read_sql("SELECT TOP 500 * FROM BMI_japanese_bmi", sql_conn)
            continue
        ct += 1

        if ct == i:
            ukbb_bmi = pd.read_sql("SELECT TOP 500 * FROM BMI_ukbb_bmi_Neale", sql_conn)
            continue
        ct += 1

        if ct == i:
            surakka = pd.read_sql("SELECT TOP 500 * FROM Lipid_Engage_Surakka_NG", sql_conn)
            continue
        ct += 1

        if ct == i:
            east_asian = pd.read_sql("SELECT TOP 500 * FROM Lipid_Exome_Lu_East_Asian_NG", sql_conn)
            continue
        ct += 1

        if ct == i:
            european = pd.read_sql("SELECT TOP 500 * FROM Lipid_Exome_Lu_European_and_East_Asian_NG", sql_conn)
            continue
        ct += 1

        if ct == i:
            glgc = pd.read_sql("SELECT TOP 500 * FROM Lipid_GLGC_Willer_NG", sql_conn)
            continue
        ct += 1

        if ct == i:
            lipid_japanese = pd.read_sql("SELECT TOP 500 * FROM Lipid_Japanese_lipid_trait_Kanai_NG", sql_conn)
            continue
        ct += 1

        if ct == i:
            lipid_mvp = pd.read_sql("SELECT TOP 500 * FROM Lipid_MVP_Klarin_NG", sql_conn)
            continue
        ct += 1

        if ct == i:
            lipid_spracklen = pd.read_sql("SELECT TOP 500 * FROM Lipid_Spracklen_Hum_Mol_Genetics", sql_conn)
            continue
        ct += 1

        if ct == i:
            high_chol = pd.read_sql("SELECT TOP 500 * FROM Lipid_UKBB_high_cholesterol_ukbb_Connor_alkesgroup", sql_conn)
            continue
        ct += 1

        if ct == i:
            ukbb_lipid = pd.read_sql("SELECT TOP 500 * FROM Lipid_UKBB_lipid_trait_Neale", sql_conn)
            continue
        ct += 1

        if ct == i:
            ukbb_statin = pd.read_sql("SELECT TOP 500 * FROM Lipid_UKBB_statin_usage_Neale", sql_conn)
            continue

    #Makes all gene names into lower cases since SQL is not case-sensitive, but Python is.
    hg19['gene_name'] = hg19['gene_name'].str.lower()
    hg19['table_name'] = 'aw011738'

    table_list = [giant,japanese,ukbb_bmi,surakka,east_asian,european,glgc,lipid_japanese,lipid_mvp,lipid_spracklen,high_chol,ukbb_lipid,ukbb_statin]
    table_name = ["giant","japanese","ukbb_bmi","surakka","east_asian","european","glgc","lipid_japanese","lipid_mvp","lipid_spracklen","high_chol","ukbb_lipid","ukbb_statin"]

    gene_name = input("Type gene name: ").lower()
    start = min(hg19.loc[(hg19['gene_name']==gene_name)]['chr_start'])
    end   = max(hg19.loc[(hg19['gene_name']==gene_name)]['chr_end'])
    chr   = hg19.loc[(hg19['gene_name']==gene_name)]['chr'].unique()

    #construct empty dataframe
    df_col = ["bp", "chr", "beta", "p_value", "trait", "table_name"]
    df = pd.DataFrame(columns=df_col)

    count=0
    for table in table_list:
        try:
            #Add a column named 'table_name' whose values are corresponding table name
            table['table_name'] = table_name[count]

            #each column that satisfies the conditions.
            a = table.loc[(start <= table['bp']) & (table['bp'] <= end)]['bp'].to_frame()
            b = table.loc[(start <= table['bp']) & (table['bp'] <= end)]['chr'].to_frame()
            c = table.loc[(start <= table['bp']) & (table['bp'] <= end)]['beta'].to_frame()
            d = table.loc[(start <= table['bp']) & (table['bp'] <= end)]['p_value'].to_frame()
            e = table.loc[(start <= table['bp']) & (table['bp'] <= end)]['trait'].to_frame()
            f = table.loc[(start <= table['bp']) & (table['bp'] <= end)]['table_name'].to_frame()

            #merge these all together
            df_temp = a.join(b).join(c).join(d).join(e).join(f)


            df = df.append(df_temp)
            count+=1

        except TypeError:
            continue

    #Convert 'bp' into integer
    df['bp'] = df['bp'].astype(int)
    #Drop irrelevant rows: chr which does not fall into the selected gene name
    df = df.loc[df['chr'].isin(chr)]
    print(df)
    print('')
