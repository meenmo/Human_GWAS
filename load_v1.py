import pandas as pd
import pyodbc

while True:
    #Connect to SQL Server
    sql_conn =  pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=PARKSLAB;DATABASE=Human_GWAS;Trusted_Connection=Yes')

    while True:

        #prompt to get input which table to include
        choose_table = input("Which tables do you want to include?\n\n 1. BMI_giant_bmi\n 2. BMI_japanese_bmi \n 3. BMI_ukbb_bmi_Neale \n  4. Lipid_Engage_Surakka_NG \n 5. Lipid_Exome_Lu_East_Asian_NG \n 6. Lipid_Exome_Lu_European_and_East_Asian_NG \n 7. Lipid_GLGC_Willer_NG \n 8. Lipid_Japanese_lipid_trait_Kanai_NG \n 9. Lipid_MVP_Klarin_NG \n 10.Lipid_Spracklen_Hum_Mol_Genetics \n 11.Lipid_UKBB_high_cholesterol_ukbb_Connor_alkesgroup \n 12.Lipid_UKBB_lipid_trait_Neale \n 13.Lipid_UKBB_statin_usage_Neale\n\nEnter the table numbers that you want to include seperataed by comma.\ne.g.) 1,3,5\nIf you want to choose all tables, then enter *.\n")

        #Obtain index of chosen tables as a list
        try:
            #select all
            if choose_table == '*':
                chosen_list = [i for i in range(1,14)]
                print(type(chosen_list))
                break

            #select multiple tables
            elif ',' in choose_table:
                chosen_list = [int(i) for i in choose_table.split(",")]
                if False not in [i in range(1,14) for i in chosen_list]:
                    break

            #select single table
            elif int(choose_table) in [i for i in range(1,14)]:
                chosen_list = [int(choose_table)]


                break
            

        except ValueError:
            print('Please enter valid input!')
            print('')
            continue


    table_list = []
    table_name = []
    for i in chosen_list:
        count = 1

        if count == i:
            giant = pd.read_sql("SELECT * FROM BMI_giant_bmi", sql_conn)
            table_list.append(giant)
            table_name.append('giant')
            continue

        count += 1
        if count == i:
            japanese = pd.read_sql("SELECT * FROM BMI_japanese_bmi", sql_conn)
            table_list.append(japanese)
            table_name.append('japanese')
            continue

        count += 1
        if count == i:
            ukbb_bmi = pd.read_sql("SELECT * FROM BMI_ukbb_bmi_Neale", sql_conn)
            table_list.append(ukbb_bmi)
            table_name.append('ukbb_bmi')
            continue

        count += 1
        if count == i:
            surakka = pd.read_sql("SELECT * FROM Lipid_Engage_Surakka_NG", sql_conn)
            table_list.append(surakka)
            table_name.append('surakka')
            continue

        count += 1
        if count == i:
            east_asian = pd.read_sql("SELECT * FROM Lipid_Exome_Lu_East_Asian_NG", sql_conn)
            table_list.append(east_asian)
            table_name.append('east_asian')
            continue

        count += 1
        if count == i:
            european = pd.read_sql("SELECT * FROM Lipid_Exome_Lu_European_and_East_Asian_NG", sql_conn)
            table_list.append(european)
            table_name.append('european')
            continue

        count += 1
        if count == i:
            glgc = pd.read_sql("SELECT * FROM Lipid_GLGC_Willer_NG", sql_conn)
            table_list.append(glgc)
            table_name.append('glgc')
            continue

        count += 1
        if count == i:
            lipid_japanese = pd.read_sql("SELECT * FROM Lipid_Japanese_lipid_trait_Kanai_NG", sql_conn)
            table_list.append(lipid_japanese)
            table_name.append('lipid_japanese')
            continue

        count += 1
        if count == i:
            lipid_mvp = pd.read_sql("SELECT * FROM Lipid_MVP_Klarin_NG", sql_conn)
            table_list.append(lipid_mvp)
            table_name.append('lipid_mvp')
            continue

        count += 1
        if count == i:
            lipid_spracklen = pd.read_sql("SELECT * FROM Lipid_Spracklen_Hum_Mol_Genetics", sql_conn)
            table_list.append(lipid_spracklen)
            table_name.append('lipid_spracklen')
            continue

        count += 1
        if count == i:
            high_chol = pd.read_sql("SELECT * FROM Lipid_UKBB_high_cholesterol_ukbb_Connor_alkesgroup", sql_conn)
            table_list.append(high_chol)
            table_name.append('high_chol')
            continue

        count += 1
        if count == i:
            ukbb_lipid = pd.read_sql("SELECT * FROM Lipid_UKBB_lipid_trait_Neale", sql_conn)
            table_list.append(ukbb_lipid)
            table_name.append('ukbb_lipid')
            continue

        count += 1
        if count == i:
            ukbb_statin = pd.read_sql("SELECT * FROM Lipid_UKBB_statin_usage_Neale", sql_conn)
            table_list.append(ukbb_statin)
            table_name.append('ukbb_statin')


    hg19 = pd.read_sql("SELECT * FROM hg19", sql_conn)
    #Makes all gene names into lower cases since SQL is not case-sensitive, but Python is.
    hg19['gene_name'] = hg19['gene_name'].str.lower()
    hg19['table_name'] = 'aw011738'

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
            a = table.loc[(start <= table['bp']) & (table['bp'] <= end) & (table['chr'].isin(chr))]['bp'].to_frame()
            b = table.loc[(start <= table['bp']) & (table['bp'] <= end) & (table['chr'].isin(chr))]['chr'].to_frame()
            c = table.loc[(start <= table['bp']) & (table['bp'] <= end) & (table['chr'].isin(chr))]['beta'].to_frame()
            d = table.loc[(start <= table['bp']) & (table['bp'] <= end) & (table['chr'].isin(chr))]['p_value'].to_frame()
            e = table.loc[(start <= table['bp']) & (table['bp'] <= end) & (table['chr'].isin(chr))]['trait'].to_frame()
            f = table.loc[(start <= table['bp']) & (table['bp'] <= end) & (table['chr'].isin(chr))]['table_name'].to_frame()

            #merge these all together
            df_temp = a.join(b).join(c).join(d).join(e).join(f)

            df = df.append(df_temp)
            count+=1

            except TypeError:
            continue

    #Convert 'bp' into integer
    df['bp'] = df['bp'].astype(int)
    #Drop irrelevant rows: chr which does not fall into the selected gene name
    #df = df.loc[df['chr'].isin(chr)]
    #print(df)
    #print('')
    print(df)
