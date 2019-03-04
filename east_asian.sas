libname sasdata "E:\SAS_Library";

%macro EA(path, dataset, trait);
data &dataset (keep = rsid beta p_value trait chr bp);
	infile &path delimiter='09'x TRUNCOVER DSD firstobs=2;

	* set length and informat and output order;
  	informat chr $2.
   	 		 bp 8.
			 SNP_hg19 $50.
			 rsid $11.
		     A1 A2 $1.
		     beta se N p_value Freq_A1_1000G_EAS 8.
 		     trait $10.;

  * read data in input order;
  input    SNP_hg19
		   rsid
		   A1 A2
		   beta se N p_value Freq_A1_1000G_EAS
 		   trait;

  trait = &trait;

  chr = compress(scan(snp_hg19, 1, ':'),'chr');
  bp  = input(scan(snp_hg19, 2, ':'),32.);

run;
%mend EA;

%EA("E:\John Li data\gwas-download-master\Plasma-Lipids_Lu_2017\EastAsian_exome_HDL.txt", EA_HDL, 'EA_HDL')
%EA("E:\John Li data\gwas-download-master\Plasma-Lipids_Lu_2017\EastAsian_exome_LDL.txt", EA_LDL, 'EA_LDL')
%EA("E:\John Li data\gwas-download-master\Plasma-Lipids_Lu_2017\EastAsian_exome_TC.txt", EA_TC, 'EA_TC')
%EA("E:\John Li data\gwas-download-master\Plasma-Lipids_Lu_2017\EastAsian_exome_TG.txt", EA_TG, 'EA_TG')


data sasdata.EA;
	length chr $2 bp  8;

	set EA_HDL EA_LDL EA_TC EA_TG;
	rsid = trim(rsid);

	array change _numeric_;
		do over change;
			if change = . then change = 0;
		end;
run;

proc export data=sasdata.EA
    outfile="E:\SAS_Export\East_Asian.csv"
    dbms=csv
    replace;
run;
