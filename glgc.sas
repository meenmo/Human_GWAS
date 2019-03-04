/*libname GWAS odbc noprompt = "server=PARKSLAB;DRIVER=SQL Server Native Client 11.0;						*/
/*		Trusted_Connection=yes" DATABASE = PARKSLAB schema = dbo;*/

libname sasdata "E:\SAS_Library";

%macro cleanup_raw(path, dataset, trait);
data &dataset (keep = rsid beta p_value trait chr bp);
	infile &path delimiter='09'x TRUNCOVER DSD firstobs=2;
	* set length and informat and output order;
  	informat chr $2.
		   	 bp 8.
			 SNP_hg18 $1.
			 SNP_hg19 $50.
			 rsid $11.
		     A1 A2 $1.
		     beta se p_value N Freq_A1_1000G_EUR 8.
 		     trait $3.;

  * read data in input order;
  input    SNP_hg18
		   SNP_hg19
		   rsid
		   A1 A2
		   beta se N p_value Freq_A1_1000G_EUR
 		   trait ;

  trait = &trait;

  chr = compress(scan(snp_hg19, 1, ':'),'chr');
  bp  = input(scan(snp_hg19, 2, ':'),32.);

run;



%mend cleanup_raw;

%cleanup_raw("E:\HUMAN_GWAS_GLGC_DATA\jointGwasMc_HDL.txt", HDL, 'HDL')
%cleanup_raw("E:\HUMAN_GWAS_GLGC_DATA\jointGwasMc_LDL.txt", LDL, 'LDL')
%cleanup_raw("E:\HUMAN_GWAS_GLGC_DATA\jointGwasMc_TC.txt", TC, 'TC')
%cleanup_raw("E:\HUMAN_GWAS_GLGC_DATA\jointGwasMc_TG.txt", TG, 'TG')

data sasdata.GLGC;
	set HDL LDL TC TG;
	rsid = trim(rsid);
	length chr $2 bp  8;
run;

proc export data=sasdata.GLGC
    outfile="E:\SAS_Export\GLGC.csv"
    dbms=csv
    replace;
run;
