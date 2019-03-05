libname sasdata "E:\SAS\SAS_Library";

%macro mvp(dataset, trait, path);
data &dataset(keep = chr bp beta p_value trait);

	infile &path delimiter='09'x TRUNCOVER DSD firstobs=23;

	/*read data in input order*/
	input  ID
	       Analysis_ID
	       rsid$
	       p_value
	       Rank
	       Plot
	       chr
	       bp
	       Submitted_SNP_ID$
	       ss2rs
	       rs2genome
	       Allele1$
	       Allele2$
	       Minor_allele$
	       pHWE$
	       Call_Rate$
	       beta
	       SE
	       R_Squared
	       Coded_Allele$
	       Sample_size
	       Bin_ID
	       ;

	trait  = &trait;
run;
%mend mvp;

%mvp(mvp_hdl,'hdl',"E:\John Li data\gwas-download-master\MVP_LIPID_DATA\hdl.txt")
%mvp(mvp_ldl,'hdl',"E:\John Li data\gwas-download-master\MVP_LIPID_DATA\ldl.txt")
%mvp(mvp_tc,'hdl',"E:\John Li data\gwas-download-master\MVP_LIPID_DATA\tc.txt")
%mvp(mvp_tg,'hdl',"E:\John Li data\gwas-download-master\MVP_LIPID_DATA\tg.txt")


data sasdata.mvp_lipid;
	set mvp_hdl mvp_ldl mvp_tc mvp_tg;
run;
