import pandas as pd
import pyodbc
import os

def error_messeage():
    print("""
          ***********************************
          *****Please enter valid input!*****
          ***********************************
          """)


def get_table():
# This function is to get a 'list' containing indices of tables to be included from user

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
13.Lipid_UKBB_statin_usage_Neale

Press 'ENTER' to include all tables.
Otherwise, enter the table numbers that you want to include seperataed by comma. e.g.) 1,3,5
""")

        #Obtain index of chosen tables as a list
        try:
            #select all
            if choose_table == '':
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
# This function is to get a 'list' of chromosome to be included from user

    while True:
        choose_chr = input("""
Press "ENTER' to include all chromosomes. 
Otherwise, enter chromosomes you want to include separate by comma.:\n""")

        # Valid input list for chromosome
        chr_list   = list(range(1,24))

        #Obtain index of chosen tables as a list
        try:
            #select all
            if choose_chr == '':
                chosen_chr = chr_list
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


def get_margin():
    defaultMarg = 200000
    while True:
        try:
            margin = int(input("Enter your margin...(Input 0 to use default value of 200,000):"))
            if margin == defaultMarg:
                break
            else:
                 break

        except ValueError:
            print('Enter a valid input.\n')

    return(margin)

def get_genename():
    gene_name    = input("Type gene name: ").lower()

    if ',' in gene_name:
        print('yes')
        return(list(set([i.replace(' ','') for i in gene_name.split(",")])))

    else:
        return([gene_name])


def get_pvalue():
    default = 0.5

    cutoff = float(input("Enter the cutoff for p-value...(Input 0 to use the default value of 0.5):"))
    while cutoff == default:
        break
    while (cutoff<0) or (cutoff > 1):
        try:
            print('Enter a valid input.\n')
            cutoff = float(input("Enter the cutoff for p-value...(Input 0 to use the default value of 0.5):"))
            break

        except ValueError:
            print('Enter a valid input.\n')

    return(cutoff)


def where(hg19,cutoff):
    chr_list = list(set(hg19['chr'].tolist()))
    where = "("
    for chr in chr_list:
        where += "chr = \'%s\'" %(chr)

        if chr_list.index(chr) != len(chr_list)-1:
            where += " or "

    where += ") and ("
    for i in range(len(hg19)):
        where += "(bp between %d and %d)" %(hg19['adj_chr_start'][i], hg19['adj_chr_end'][i])

        if i != len(hg19)-1:
            where += ' or '

    where += ") and (p_value < %f)" %(cutoff)

    return(where)


def where_varchar(hg19, cutoff):
# This function is exactly same as 'def where'
# But for the table whose p_value column is stored as varchar
    chr_list = list(set(hg19['chr'].tolist()))
    where = "("
    for chr in chr_list:
        where += "chr = \'%s\' " %(chr)

        if chr_list.index(chr) != len(chr_list)-1:
            where += "or "

    where += ") and ("
    for i in range(len(hg19)):
        where += "(bp between %d and %d)" %(hg19['adj_chr_start'][i], hg19['adj_chr_end'][i])

        if i != len(hg19)-1:
            where += ' or '

    where += ") and (p_value < \'%f\')" %(cutoff)

    return(where)


def get_df(sql_conn, hg19, chosen_table, margin, cutoff):
    df = pd.DataFrame(columns=["chr", "bp", "beta", "p_value", "trait", "table_name"])
    for i in chosen_table:
        ct = 1
        if ct == i:
            query = "SELECT chr, bp, beta, p_value, trait, 'BMI_giant_bmi' as table_name FROM BMI_giant_bmi WHERE "
            query += where(hg19,cutoff)
            giant = pd.read_sql(query, sql_conn)
            giant = giant.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df = df.append(giant)
            continue

        ct += 1
        if ct == i:
            query = "SELECT chr, bp, beta, p_value, trait, 'BMI_japanese_bmi' as table_name FROM BMI_japanese_bmi WHERE "
            query +=where(hg19,cutoff)
            japanese = pd.read_sql(query, sql_conn)
            japanese = japanese.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df = df.append(japanese)
            continue
        ct += 1

        if ct == i:
            query = "SELECT chr, bp, beta, p_value, trait, 'BMI_ukbb_bmi_Neale' as table_name FROM BMI_ukbb_bmi_Neale WHERE "
            query +=where(hg19,cutoff)
            ukbb_bmi = pd.read_sql(query, sql_conn)
            ukbb_bmi = ukbb_bmi.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df = df.append(ukbb_bmi)
            continue
        ct += 1

        if ct == i:
            query = "SELECT chr, bp, beta, p_value, trait, 'Lipid_Engage_Surakka_NG' as table_name FROM Lipid_Engage_Surakka_NG WHERE "
            query += where_varchar(hg19, cutoff)
            surakka = pd.read_sql(query, sql_conn)
            surakka = surakka.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df = df.append(surakka)
            continue
        ct += 1

        if ct == i:
            query = "SELECT chr, bp, beta, p_value, trait, 'Lipid_Exome_Lu_East_Asian_NG' as table_name FROM Lipid_Exome_Lu_East_Asian_NG WHERE "
            query +=where(hg19,cutoff)
            east_asian = pd.read_sql(query, sql_conn)
            east_asian = east_asian.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df = df.append(east_asian)
            continue
        ct += 1

        if ct == i:
            query = "SELECT chr, bp, beta, p_value, trait, 'Lipid_Exome_Lu_European_and_East_Asian_NG' as table_name FROM Lipid_Exome_Lu_European_and_East_Asian_NG WHERE "
            query +=where(hg19,cutoff)
            european = pd.read_sql(query, sql_conn)
            european = european.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df = df.append(european)
            continue
        ct += 1

        if ct == i:
            query = "SELECT chr, bp, beta, p_value, trait, 'Lipid_GLGC_Willer_NG' as table_name FROM Lipid_GLGC_Willer_NG WHERE "
            query +=where(hg19,cutoff)
            glgc = pd.read_sql(query, sql_conn)
            glgc = glgc.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df = df.append(glgc)
            continue
        ct += 1

        if ct == i:
            query = "SELECT chr, bp, beta, p_value, trait, 'Lipid_Japanese_lipid_trait_Kanai_NG' as table_name FROM Lipid_Japanese_lipid_trait_Kanai_NG WHERE "
            query +=where_varchar(hg19,cutoff)
            lipid_japanese = pd.read_sql(query, sql_conn)
            lipid_japanese = lipid_japanese.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df = df.append(lipid_japanese)
            continue
        ct += 1

        if ct == i:
            query = "SELECT chr, bp, beta, p_value, trait, 'Lipid_MVP_Klarin_NG' as table_name FROM Lipid_MVP_Klarin_NG WHERE "
            query +=where(hg19,cutoff)
            lipid_mvp = pd.read_sql(query, sql_conn)
            lipid_mvp = lipid_mvp.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df = df.append(lipid_mvp)
            continue
        ct += 1

        if ct == i:
            query = "SELECT chr, bp, beta, p_value, trait, 'Lipid_Spracklen_Hum_Mol_Genetics' as table_name FROM Lipid_Spracklen_Hum_Mol_Genetics WHERE "
            query +=where_varchar(hg19,cutoff)
            lipid_spracklen = pd.read_sql(query, sql_conn)
            lipid_spracklen = lipid_spracklen.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df = df.append(lipid_spracklen)
            continue
        ct += 1

        if ct == i:
            query = "SELECT chr, bp, beta, p_value, trait, 'Lipid_UKBB_high_cholesterol_ukbb_Connor_alkesgroup' as table_name FROM Lipid_UKBB_high_cholesterol_ukbb_Connor_alkesgroup WHERE "
            query +=where_varchar(hg19,cutoff)
            high_chol = pd.read_sql(query, sql_conn)
            high_chol = high_chol.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df = df.append(high_chol)
            continue
        ct += 1

        if ct == i:
            query = "SELECT chr, bp, beta, p_value, trait, 'Lipid_UKBB_lipid_trait_Neale' as table_name FROM Lipid_UKBB_lipid_trait_Neale WHERE "
            query +=where(hg19,cutoff)
            ukbb_lipid_trait = pd.read_sql(query, sql_conn)
            ukbb_lipid_trait = ukbb_lipid_trait.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df = df.append(ukbb_lipid_trait)
            continue
        ct += 1

        if ct == i:
            query = "SELECT chr, bp, beta, p_value, trait, 'Lipid_UKBB_statin_usage_Neale' as table_name FROM Lipid_UKBB_statin_usage_Neale WHERE "
            query +=where(hg19,cutoff)
            ukbb_statin = pd.read_sql(query, sql_conn)
            ukbb_statin = ukbb_statin.astype({"chr": "category", "bp": "int64", "beta": "float64",  "p_value": "float64", "table_name": "category"})
            df = df.append(ukbb_statin)
            continue

    return(df)


def get_hg19(sql_conn, gene_name, margin):
# This will spits out 'hg19' table with chosen chromosome and gene_name

#     for chr in chosen_chr:
#         where += "chr = \'%s\' " %(chr)

#         if chosen_chr.index(chr) != len(chosen_chr)-1:
#             where += "or "

    # where += ") and ("
    
    # concatenating a condition regarding 'gene_name'
    where = "("
    for gene_i in gene_name:
        where      += "gene_name = \'%s\'" %(gene_i)

        if gene_name.index(gene_i) != len(gene_name)-1:
            where += "or "

    where += ")"

    # concatenating 'where' statement and modify the interval of 'chr_start' and 'chr_end'
    query_hg19 = """
                 SELECT chr, gene_name, chr_start - %d as 'adj_chr_start',
                        chr_end + %d as 'adj_chr_end', 'hg19' as table_name
                 FROM hg19
                 WHERE """ %(margin, margin) + where


    hg19 = pd.read_sql(query_hg19, sql_conn)
    hg19 = hg19.astype({"chr": "category","adj_chr_start": "int64", "adj_chr_end": "int64", "table_name": "category"})

    return(hg19)


def save_option(df):
    option = input("""How do you want to save this result?
1. Save as csv file
2. Nothing:\n""")
    while option not in ['1','2','3']:
        print("Enter a valid input\n")
        option = input("""How do you want to save this result?
1. Save as csv file
2. Nothing:\n""")

    try:
        if option == '1':
            path = 'E:/cross_ref/cross_ref.csv'
            df.to_csv(path, encoding = 'utf-8', index=False)
            os.startfile(path)

    except PermissionError:
        print('Close the csv file currently opened and try again')
        pass

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

#         chosen_chr   = get_chr()
#         print('')
        
        # please put your file path
        
        gene_name    = get_genename()
        print('')

        margin       = get_margin()
        print('')

        cutoff       = get_pvalue()


        hg19 = get_hg19(sql_conn, gene_name, margin)
        df   = get_df(sql_conn, hg19, chosen_table, margin, cutoff)

        print(df.to_string())
        save_option(df)


if __name__ == "__main__":
    main()
