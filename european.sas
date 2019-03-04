libname sasdata "E:\SAS_Library";

%macro EU(path, dataset, trait);
data &dataset (keep = rsid beta p_value trait chr bp);
	infile &path delimiter='09'x TRUNCOVER DSD firstobs=2;
	* set length and informat and output order;
  	informat chr $2.
		   	 bp 8.
			 SNP_hg19 $50.
			 rsid $11.
		     A1 A2 $1.
		     beta se N p_value Freq_A1 8.
 		     trait $6.;

  * read data in input order;
  input    SNP_hg19
		   rsid
		   A1 A2
		   beta se N p_value Freq_A1
 		   trait ;

  trait = &trait;

  chr = compress(scan(snp_hg19, 1, ':'),'chr');
  bp  = input(scan(snp_hg19, 2, ':'),32.);

run;
%mend EU;

%EU("E:\John Li data\gwas-download-master\Plasma-Lipids_Lu_2017\European_EastAsian_exome_HDL.txt", EU_HDL, 'EU_HDL')
%EU("E:\John Li data\gwas-download-master\Plasma-Lipids_Lu_2017\European_EastAsian_exome_LDL.txt", EU_LDL, 'EU_LDL')
%EU("E:\John Li data\gwas-download-master\Plasma-Lipids_Lu_2017\European_EastAsian_exome_TC.txt", EU_TC, 'EU_TC')
%EU("E:\John Li data\gwas-download-master\Plasma-Lipids_Lu_2017\European_EastAsian_exome_TG.txt", EU_TG, 'EU_TG')

data sasdata.EU;

	set EU_HDL EU_LDL EU_TC EU_TG;
	rsid = trim(rsid);

	array change _numeric_;
	do over change;
		if change = . then change = 0;
	end;
run;

proc export data=sasdata.EU
    outfile="E:\SAS_Export\European.csv"
    dbms=csv
    replace;
run;
