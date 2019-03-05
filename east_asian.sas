libname sasdata "E:\SAS\SAS_Library";

%macro EA(path, dataset, trait);
data &dataset (keep = rsid beta p_value trait chr bp);
   /*set the enough lenth for longer variables*/
   length SNP_hg19 rsid$20;

   /*'09'x refers to tab delimiter*/
   infile &path delimiter='09'x TRUNCOVER DSD firstobs=2;

  /*read data in input order*/
  input    SNP_hg19$
           rsid$
           A1$ A2$
           beta se N p_value Freq_A1_1000G_EAS
           ;

  trait = &trait;

  /*split into chr and bp by delimeter :*/
  chr = compress(scan(snp_hg19, 1, ':'),'chr');
  bp  = input(scan(snp_hg19, 2, ':'),32.);

run;
%mend EA;


%EA("E:\John Li data\gwas-download-master\LIPID\Plasma-Lipids_Lu_2017\EastAsian_exome_HDL.txt", EA_HDL, 'HDL')
%EA("E:\John Li data\gwas-download-master\LIPID\Plasma-Lipids_Lu_2017\EastAsian_exome_LDL.txt", EA_LDL, 'LDL')
%EA("E:\John Li data\gwas-download-master\LIPID\Plasma-Lipids_Lu_2017\EastAsian_exome_TC.txt", EA_TC, 'TC')
%EA("E:\John Li data\gwas-download-master\LIPID\Plasma-Lipids_Lu_2017\EastAsian_exome_TG.txt", EA_TG, 'TG')


/*Merge into a single table*/
data sasdata.East_Asian;
	length chr $2;
	set EA_HDL EA_LDL EA_TC EA_TG;
run;
