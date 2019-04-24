import pandas as pd
import pyodbc

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


    return([str(i) for i in chosen_chr])


def main():
    # Connect to SQL Server
    sql_conn =  pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=PARKSLAB;DATABASE=Human_GWAS;Trusted_Connection=Yes')

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

        query_hg19 = """
                     SELECT *, 'hg19' as table_name
                     FROM hg19
                     WHERE """ %(    )

        # This is to concatenate where condition based on chosen_chr
        for chr in chosen_chr:
            query_hg19 += "chr = \'%s\' "

            if list.index(chr) != len(chosen_chr)-1:
                query_hg19 += "or "


        hg19 = pd.read_sql(query_hg19, sql_conn)
        # Make all gene names to be lower case
        hg19['gene_name'] = hg19['gene_name'].str.lower()
        # The starting and end location of chromosome of corresponding gene name under hg19
        start = min(hg19.loc[(hg19['gene_name']==gene_name)]['chr_start']) - margin
        end   = max(hg19.loc[(hg19['gene_name']==gene_name)]['chr_end']) + margin

        table_dic = {}
        for i in chosen_table:
            ct = 1

            if ct == i:
                giant = pd.read_sql("SELECT *, 'giant' as table_name FROM BMI_giant_bmi", sql_conn)
                table_dic[ct] = [giant, "giant"]
                continue
            ct += 1

            if ct == i:
                japanese = pd.read_sql("SELECT TOP 500 *, 'japanese_bmi' as table_name FROM BMI_japanese_bmi", sql_conn)
                table_dic[ct] = [japanese,"japanese"]
                continue
            ct += 1

            if ct == i:
                ukbb_bmi = pd.read_sql("SELECT TOP 500 *, 'bmi_ukbb' as table_name FROM BMI_ukbb_bmi_Neale", sql_conn)
                table_dic[ct] = [ukbb_bmi,"ukbb_bmi"]
                continue
            ct += 1

            if ct == i:
                surakka = pd.read_sql("SELECT TOP 500 *, 'surakka' as table_name FROM Lipid_Engage_Surakka_NG", sql_conn)
                table_dic[ct] = [surakka,"surakka"]
                continue
            ct += 1

            if ct == i:
                east_asian = pd.read_sql("SELECT TOP 500 *, 'east_asian' as table_name FROM Lipid_Exome_Lu_East_Asian_NG", sql_conn)
                table_dic[ct] = [east_asian,"east_asian"]
                continue
            ct += 1

            if ct == i:
                european = pd.read_sql("SELECT TOP 500 *, 'european' as table_name FROM Lipid_Exome_Lu_European_and_East_Asian_NG", sql_conn)
                table_dic[ct] = [european,"european"]
                continue
            ct += 1

            if ct == i:
                glgc = pd.read_sql("SELECT TOP 500 *, 'glgc' as table_name FROM Lipid_GLGC_Willer_NG", sql_conn)
                table_dic[ct] = [glgc,"glgc"]
                continue
            ct += 1

            if ct == i:
                lipid_japanese = pd.read_sql("SELECT TOP 500 *, 'japanese_lipid' as table_name FROM Lipid_Japanese_lipid_trait_Kanai_NG", sql_conn)
                table_dic[ct] = [lipid_japanese,"lipid_japanese"]
                continue
            ct += 1

            if ct == i:
                lipid_mvp = pd.read_sql("SELECT TOP 500 *, 'lipid_mvp' as table_name FROM Lipid_MVP_Klarin_NG", sql_conn)
                table_dic[ct] = [lipid_mvp,"lipid_mvp"]
                continue
            ct += 1

            if ct == i:
                lipid_spracklen = pd.read_sql("SELECT TOP 500 *, 'lipid_spracklen' as table_name FROM Lipid_Spracklen_Hum_Mol_Genetics", sql_conn)
                table_dic[ct] = [lipid_spracklen,"lipid_spracklen"]
                continue
            ct += 1

            if ct == i:
                high_chol = pd.read_sql("SELECT TOP 500 *, 'high_chol' as table_name FROM Lipid_UKBB_high_cholesterol_ukbb_Connor_alkesgroup", sql_conn)
                table_dic[ct] = [high_chol,"high_chol"]
                continue
            ct += 1

            if ct == i:
                ukbb_lipid_trait = pd.read_sql("SELECT TOP 500 *, 'ukbb_lipid_trait' as table_name FROM Lipid_UKBB_lipid_trait_Neale", sql_conn)
                table_dic[ct] = [ukbb_lipid_trait,"ukbb_lipid_trait"]
                continue
            ct += 1

            if ct == i:
                ukbb_statin = pd.read_sql("SELECT TOP 500 *, 'ukbb_statin' as table_name FROM Lipid_UKBB_statin_usage_Neale", sql_conn)
                table_dic[ct] = [ukbb_statin,"ukbb_statin"]
                continue
        # Construct empty dataframe
        df = pd.DataFrame(columns=["bp", "chr", "beta", "p_value", "trait", "table_name"])
        #df.append(pd.DataFrame(data).reindex(columns=df.columns))

        # Table dictionary


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

                # merge these all together
                df_temp   = a.join(b).join(c).join(d).join(e)
                # .join(f)

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
