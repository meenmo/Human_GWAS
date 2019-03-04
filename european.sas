libname sasdata "E:\SAS\SAS_Library";

%macro EU(path, dataset, trait);
data &dataset (keep = rsid beta p_value trait chr bp);
	length SNP_hg19 rsid $20;

	infile &path delimiter='09'x TRUNCOVER DSD firstobs=2;

	/*read data in input order; variable with $ is chracter, without is numeric*/
	input    SNP_hg19$
		     rsid$
		     A1$ A2$
		     beta se N p_value Freq_A1
	 	     ;

	trait = &trait;

	chr = compress(scan(snp_hg19, 1, ':'),'chr');
	bp  = input(scan(snp_hg19, 2, ':'),32.);

run;
%mend EU;


%EU("E:\John Li data\gwas-download-master\LIPID\Plasma-Lipids_Lu_2017\European_EastAsian_exome_HDL.txt", EU_HDL, 'HDL')
%EU("E:\John Li data\gwas-download-master\LIPID\Plasma-Lipids_Lu_2017\European_EastAsian_exome_LDL.txt", EU_LDL, 'LDL')
%EU("E:\John Li data\gwas-download-master\LIPID\Plasma-Lipids_Lu_2017\European_EastAsian_exome_TC.txt", EU_TC, 'TC')
%EU("E:\John Li data\gwas-download-master\LIPID\Plasma-Lipids_Lu_2017\European_EastAsian_exome_TG.txt", EU_TG, 'TG')


/*merge into a single table*/
data sasdata.EU;
	length chr$2;
	set EU_HDL EU_LDL EU_TC EU_TG;
run;

