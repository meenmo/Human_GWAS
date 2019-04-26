import pandas as pd
import pyodbc

def error_messeage():
    print("""
          ***********************************
          *****Please enter valid input!*****
          ***********************************
          """)


def get_table():
# 
# This function is to get a 'list' containing the numbers corresponding to each table from user
# 
    while True:
        # It prompts to get input asking which table to include        
        choose_table = input("""
Which tables do you want to include?\n
1. BMI_giant_bmi
2. BMI_japanese_bmi
3. BMI_ukbb_bmi_Neale
4. Lipid_Engage_Surakka_NG
5. Lipid_Exome_Lu_East_Asian_NG
6. Lipid_Exome_Lu_European_and_East_Asian_NG
7. Lipid_GLGC_Willer_NG
8. Lipid_Japanese_lipid_trait_Kanai_NG
9. Lipid_MVP_Klarin_NG
10.Lipid_Spracklen_Hum_Mol_Genetics
11.Lipid_UKBB_high_cholesterol_ukbb_Connor_alkesgroup
12.Lipid_UKBB_lipid_trait_Neale
13.Lipid_UKBB_statin_usage_Neale\n
Enter the table numbers that you want to include seperataed by comma. e.g.) 1,3,5
If you want to choose all tables, then enter *.""")

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

            #select a single table
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
#
# This function is to get a 'list' of chromosome numbers from user
#   
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

            #select a single table
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


def where(chosen_chr, cutoff):
#
# This function is to get a 'condition statement as a string' of sql query.
# This will be concatanated after existing query string in the main function and df function below.
# Sample output is like
# "(chr = '1' or chr = '3' or chr '6' ) and (p_value < 0.02)"
#
    where = "("
    for chr in chosen_chr:
        where += "chr = \'%s\' " %(chr)

        if chosen_chr.index(chr) != len(chosen_chr)-1:
            where += "or "

    where += ") and (p_value < %f)" %(cutoff)

    return(where)


def df(sql_conn, chosen_table, chosen_chr, margin, cutoff):
#
# This function is to get a 'single data frame' of selected table.
# Throughout the sql query, only needed observations will be selected.
# In order to improve efficiency, some colmuns are converted into better data type.
#
    df_temp = pd.DataFrame(columns=["chr", "bp", "beta", "p_value", "trait", "table_name"])
    for i in chosen_table:
        ct = 1
        if ct == i:
            query            = "SELECT chr, bp, beta, p_value, trait, 'giant' as table_name FROM BMI_giant_bmi WHERE "
            query            += where(chosen_chr,cutoff)
            giant            = pd.read_sql(query, sql_conn)
            giant            = giant.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df_temp          = df_temp.append(giant)
            continue


        ct += 1
        if ct == i:
            query            = "SELECT chr, bp, beta, p_value, trait, 'japanese_bmi' as table_name FROM BMI_japanese_bmi WHERE "
            query            +=where(chosen_chr,cutoff)
            japanese         = pd.read_sql(query, sql_conn)
            japanese         = japanese.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df_temp          = df_temp.append(japanese)
            continue
        ct += 1

        if ct == i:
            query            = "SELECT chr, bp, beta, p_value, trait, 'bmi_ukbb' as table_name FROM BMI_ukbb_bmi_Neale WHERE "
            query            +=where(chosen_chr,cutoff)
            ukbb_bmi         = pd.read_sql(query, sql_conn)
            ukbb_bmi         = ukbb_bmi.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df_temp          = df_temp.append(ukbb_bmi)
            continue
        ct += 1

        if ct == i:
            query            = "SELECT chr, bp, beta, p_value, trait, 'surakka' as table_name FROM Lipid_Engage_Surakka_NG WHERE "
            query            +=where(chosen_chr,cutoff)
            surakka          = pd.read_sql(query, sql_conn)
            surakka          = surakka.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df_temp          = df_temp.append(surakka)
            continue
        ct += 1

        if ct == i:
            query            = "SELECT chr, bp, beta, p_value, trait, 'east_asian' as table_name FROM Lipid_Exome_Lu_East_Asian_NG WHERE "
            query            +=where(chosen_chr,cutoff)
            east_asian       = pd.read_sql(query, sql_conn)
            east_asian       = east_asian.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df_temp          = df_temp.append(east_asian)
            continue
        ct += 1

        if ct == i:
            query            = "SELECT chr, bp, beta, p_value, trait, 'european' as table_name FROM Lipid_Exome_Lu_European_and_East_Asian_NG WHERE "
            query            +=where(chosen_chr,cutoff)
            european         = pd.read_sql(query, sql_conn)
            european         = european.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df_temp          = df_temp.append(european)
            continue
        ct += 1

        if ct == i:
            query            = "SELECT chr, bp, beta, p_value, trait, 'glgc' as table_name FROM Lipid_GLGC_Willer_NG WHERE "
            query            +=where(chosen_chr,cutoff)
            glgc             = pd.read_sql(query, sql_conn)
            glgc             = glgc.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df_temp          = df_temp.append(glgc)
            continue
        ct += 1

        if ct == i:
            query            = "SELECT chr, bp, beta, p_value, trait, 'japanese_lipid' as table_name FROM Lipid_Japanese_lipid_trait_Kanai_NG WHERE "
            query            +=where(chosen_chr,cutoff)
            lipid_japanese   = pd.read_sql(query, sql_conn)
            lipid_japanese   = lipid_japanese.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df_temp          = df_temp.append(lipid_japanese)
            continue
        ct += 1

        if ct == i:
            query            = "SELECT chr, bp, beta, p_value, trait, 'lipid_mvp' as table_name FROM Lipid_MVP_Klarin_NG WHERE "
            query            +=where(chosen_chr,cutoff)
            lipid_mvp        = pd.read_sql(query, sql_conn)
            lipid_mvp        = lipid_mvp.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df_temp          = df_temp.append(lipid_mvp)
            continue
        ct += 1

        if ct == i:
            query            = "SELECT chr, bp, beta, p_value, trait, 'lipid_spracklen' as table_name FROM Lipid_Spracklen_Hum_Mol_Genetics WHERE "
            query            +=where(chosen_chr,cutoff)
            lipid_spracklen  = pd.read_sql(query, sql_conn)
            lipid_spracklen  = lipid_spracklen.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df_temp          = df_temp.append(lipid_spracklen)
            continue
        ct += 1

        if ct == i:
            query            = "SELECT chr, bp, beta, p_value, trait, 'high_chol' as table_name FROM Lipid_UKBB_high_cholesterol_ukbb_Connor_alkesgroup WHERE "
            query            +=where(chosen_chr,cutoff)
            high_chol        = pd.read_sql(query, sql_conn)
            high_chol        = high_chol.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df_temp          = df_temp.append(high_chol)
            continue
        ct += 1

        if ct == i:
            query            = "SELECT chr, bp, beta, p_value, trait, 'ukbb_lipid_trait' as table_name FROM Lipid_UKBB_lipid_trait_Neale WHERE "
            query            +=where(chosen_chr,cutoff)
            ukbb_lipid_trait = pd.read_sql(query, sql_conn)
            ukbb_lipid_trait = ukbb_lipid_trait.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df_temp          = df_temp.append(ukbb_lipid_trait)
            continue
        ct += 1

        if ct == i:
            query            = "SELECT chr, bp, beta, p_value, trait, 'ukbb_statin' as table_name FROM Lipid_UKBB_statin_usage_Neale WHERE "
            query            +=where(chosen_chr,cutoff)
            ukbb_statin      = pd.read_sql(query, sql_conn)
            ukbb_statin      = ukbb_statin.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df_temp          = df_temp.append(ukbb_statin)
            continue

    return(df_temp)


def main():
    # Connect to SQL Server
    sql_conn =  pyodbc.connect("""
                               DRIVER={ODBC Driver 11 for SQL Server};
                               SERVER=PARKSLAB;
                               DATABASE=Human_GWAS;
                               Trusted_Connection=Yes;
                               """)

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

        cutoff       = float(input("Enter the cutoff for P-value: "))


        ##############################################
        ##Load hg19 w/ only chosen chr and gene_name##
        ##############################################
        
        # conditioning on 'chr'
        where = "("
        for chr in chosen_chr:
            where += "chr = \'%s\' " %(chr)

            if chosen_chr.index(chr) != len(chosen_chr)-1:
                where += "or "
        
        # concatenating a condition regarding 'gene_name'
        where      += ") and (gene_name = \'%s\')" %(gene_name)

        # concatenating 'where' statement and modify the interval of 'chr_start' and 'chr_end'
        query_hg19 = """
                     SELECT chr, gene_name, chr_start - %d as 'adj_chr_start',
                            chr_end + %d as 'adj_chr_end', 'hg19' as table_name
                     FROM hg19
                     WHERE """ %(margin, margin) + where

        
        hg19 = pd.read_sql(query_hg19, sql_conn)
        hg19 = hg19.astype({"chr": "category","adj_chr_start": "int64", "adj_chr_end": "int64", "table_name": "category"})

        df_all= df(sql_conn, chosen_table, chosen_chr, margin, cutoff)

        #hg19.sort_index(inplace=True)
        start = hg19['adj_chr_start']
        end   = hg19['adj_chr_end']


        # a = df_all.loc[(start <= df_all['bp']) & (df_all['bp'] <= end)]['chr'].to_frame()
        # b = df_all.loc[(start <= df_all['bp']) & (df_all['bp'] <= end)]['chr'].to_frame()
        # c = df_all.loc[(start <= df_all['bp']) & (df_all['bp'] <= end)]['beta'].to_frame()
        # d = df_all.loc[(start <= df_all['bp']) & (df_all['bp'] <= end)]['p_value'].to_frame()
        # e = df_all.loc[(start <= df_all['bp']) & (df_all['bp'] <= end)]['trait'].to_frame()
        # f = df_all.loc[(start <= df_all['bp']) & (df_all['bp'] <= end)]['table_name'].to_frame()
        #
        #
        # return(a.join(b).join(c).join(d).join(e))

        #df_all.sort_index(inplace=True)
        return(df_all.loc[(start <= df_all['bp']) & (df_all['bp'] <= end)])


if __name__ == "__main__":
    main()
