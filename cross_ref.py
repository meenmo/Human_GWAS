import pandas as pd
import pyodbc
import pandas.io.sql as psql

def error_messeage():
    print('')
    print('***********************************')
    print('*****Please enter valid input!*****')
    print('***********************************')
    print('')


def get_table():
    while True:
        #prompt to get input which table to include
        # choose_table = input("Which tables do you want to include?\n\n 1. BMI_giant_bmi\n 2. BMI_japanese_bmi \n 3. BMI_ukbb_bmi_Neale \n 4. Lipid_Engage_Surakka_NG \n 5. Lipid_Exome_Lu_East_Asian_NG \n 6. Lipid_Exome_Lu_European_and_East_Asian_NG \n 7. Lipid_GLGC_Willer_NG \n 8. Lipid_Japanese_lipid_trait_Kanai_NG \n 9. Lipid_MVP_Klarin_NG \n 10.Lipid_Spracklen_Hum_Mol_Genetics \n 11.Lipid_UKBB_high_cholesterol_ukbb_Connor_alkesgroup \n 12.Lipid_UKBB_lipid_trait_Neale \n 13.Lipid_UKBB_statin_usage_Neale\n\nEnter the table numbers that you want to include seperataed by comma.\ne.g.) 1,3,5\nIf you want to choose all tables, then enter *.\n")
        print("Which tables do you want to include?\n")
        print("1. BMI_giant_bmi")
        print("2. BMI_japanese_bmi")
        print("3. BMI_ukbb_bmi_Neale")
        print("4. Lipid_Engage_Surakka_NG")
        print("5. Lipid_Exome_Lu_East_Asian_NG")
        print("6. Lipid_Exome_Lu_European_and_East_Asian_NG")
        print("7. Lipid_GLGC_Willer_NG")
        print("8. Lipid_Japanese_lipid_trait_Kanai_NG")
        print("9. Lipid_MVP_Klarin_NG")
        print("10.Lipid_Spracklen_Hum_Mol_Genetics")
        print("11.Lipid_UKBB_high_cholesterol_ukbb_Connor_alkesgroup")
        print("12.Lipid_UKBB_lipid_trait_Neale")
        print("13.Lipid_UKBB_statin_usage_Neale\n")
        print("Enter the table numbers that you want to include seperataed by comma. e.g.) 1,3,5")
        print("If you want to choose all tables, then enter *.")
        choose_table = input()

        #Obtain index of chosen tables as a list
        try:
            #select all
            if choose_table == '*':
                chosen_table = [i for i in range(1,14)]
                break

            #select multiple tables
            elif ',' in choose_table:
                # The sets module provides classes for constructing and
                # manipulating unordered collections of unique elements.
                # Then cast to list again.
                chosen_table = list(set([int(i) for i in choose_table.split(",")]))

                if False not in [i in range(1,14) for i in chosen_table]:
                    break
                else:
                    error_messeage()
                    continue

            #select single table
            elif int(choose_table) in [i for i in range(1,14)]:
                chosen_table = [int(choose_table)]
                break

            else:
                error_messeage()
                continue

        except ValueError:
            error_messeage()
            continue

    return(chosen_table)


def get_chr():
    while True:
        choose_chr = input("Enter chromosomes you want to include. Separate by comma if you select multiple chromosomes:\n")
        # Valid input list for chromosome
        chr_list   = list(range(1,24))

        #Obtain index of chosen tables as a list
        try:
            #select all
            if chr == '*':
                chosen_chr = [i for i in choose_chr]
                break

            #select multiple tables
            elif ',' in choose_chr:
                # The sets module provides classes for constructing and
                # manipulating unordered collections of unique elements.
                # Then cast to list again.
                chosen_chr = list(set([int(i) for i in choose_chr.split(",")]))

                if False not in [i in chr_list for i in chosen_chr]:
                    break
                else:
                    error_messeage()
                    continue

            #select single table
            elif int(choose_chr) in [i for i in chr_list]:
                chosen_chr = [int(choose_chr)]
                break

            else:
                error_messeage()
                continue

        except ValueError:
            error_messeage()
            continue

    return(chosen_chr)


def main():
    # Connect to SQL Server
    sql_conn =  pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=PARKSLAB;DATABASE=Human_GWAS;Trusted_Connection=Yes')

    # Load tables from SQL Server
    ukbb_lipid               = pd.read_sql("SELECT * FROM Lipid_UKBB_lipid_trait_Neale", sql_conn)
    ukbb_statin              = pd.read_sql("SELECT * FROM Lipid_UKBB_statin_usage_Neale", sql_conn)
    hg19            = pd.read_sql("SELECT * FROM hg19", sql_conn)
    giant           = pd.read_sql("SELECT * FROM BMI_giant_bmi", sql_conn)
    japanese        = pd.read_sql("SELECT * FROM BMI_japanese_bmi", sql_conn)
    ukbb_bmi        = pd.read_sql("SELECT * FROM BMI_ukbb_bmi_Neale", sql_conn)
    surakka         = pd.read_sql("SELECT * FROM Lipid_Engage_Surakka_NG", sql_conn)
    east_asian      = pd.read_sql("SELECT * FROM Lipid_Exome_Lu_East_Asian_NG", sql_conn)
    european        = pd.read_sql("SELECT * FROM Lipid_Exome_Lu_European_and_East_Asian_NG", sql_conn)
    glgc            = pd.read_sql("SELECT * FROM Lipid_GLGC_Willer_NG", sql_conn)
    lipid_japanese  = pd.read_sql("SELECT * FROM Lipid_Japanese_lipid_trait_Kanai_NG", sql_conn)
    lipid_mvp       = pd.read_sql("SELECT * FROM Lipid_MVP_Klarin_NG", sql_conn)
    lipid_spracklen = pd.read_sql("SELECT * FROM Lipid_Spracklen_Hum_Mol_Genetics", sql_conn)
    high_chol       = pd.read_sql("SELECT * FROM Lipid_UKBB_high_cholesterol_ukbb_Connor_alkesgroup", sql_conn)

    # Make all gene names to be lower case
    hg19['gene_name'] = hg19['gene_name'].str.lower()
    # Add a column named 'table_name' with corresponding table name
    hg19['table_name'] = 'hg19'

    # Once all tables are loaded, we can search multiple times
    while True:
        # Input for which tables&chromosome to include and gene name and margin(+/-)
        chosen_table = get_table()
        print('')
        chosen_chr   = get_chr()
        print('')
        gene_name    = input("Type gene name: ").lower()
        print('')
        margin       = int(input("Enter your margin: "))
        print('')

        # The starting and end location of chromosome of corresponding gene name under hg19
        start = min(hg19.loc[(hg19['gene_name']==gene_name)]['chr_start']) - margin
        end   = max(hg19.loc[(hg19['gene_name']==gene_name)]['chr_end']) + margin

        # Construct empty dataframe
        df = pd.DataFrame(columns=["bp", "chr", "beta", "p_value", "trait", "table_name"])

        # Table dictionary
        table_dic = {1:[giant,"giant"], 2:[japanese,"japanese"], 3:[ukbb_bmi,"ukbb_bmi"], 4:[surakka,"surakka"], 5:[east_asian,"east_asian"], 6:[european,"european"], 7:[glgc,"glgc"], 8:[lipid_japanese,"lipid_japanese"],9:[lipid_mvp,"lipid_mvp"], 10:[lipid_spracklen,"lipid_spracklen"], 11:[high_chol,"high_chol"], 12:[ukbb_lipid,"ukbb_lipid"], 13:[ukbb_statin,"ukbb_statin"]}

        for i in chosen_table:
            try:
                table      = table_dic[i][0]
                table_name = table_dic[i][1]

                #Add a column named 'table_name' whose values are corresponding table name
                table["table_name"] = table_name

                #each column that satisfies the conditions.
                a = table.loc[(start <= table['bp']) & (table['bp'] <= end) & (table['chr'].isin(chosen_chr))]['bp'].to_frame()
                b = table.loc[(start <= table['bp']) & (table['bp'] <= end) & (table['chr'].isin(chosen_chr))]['chr'].to_frame()
                c = table.loc[(start <= table['bp']) & (table['bp'] <= end) & (table['chr'].isin(chosen_chr))]['beta'].to_frame()
                d = table.loc[(start <= table['bp']) & (table['bp'] <= end) & (table['chr'].isin(chosen_chr))]['p_value'].to_frame()
                e = table.loc[(start <= table['bp']) & (table['bp'] <= end) & (table['chr'].isin(chosen_chr))]['trait'].to_frame()
                f = table.loc[(start <= table['bp']) & (table['bp'] <= end) & (table['chr'].isin(chosen_chr))]['table_name'].to_frame()

                #merge these all together
                df_temp   = a.join(b).join(c).join(d).join(e).join(f)

                #append to the existing df
                df        = df.append(df_temp)

                #cast 'bp' column to int
                df['bp']  = df['bp'].astype(int)
                df['chr'] = df['chr'].astype(int)

            except TypeError:
                continue

        print(df)
        print('')



if __name__ == "__main__":
    main()
