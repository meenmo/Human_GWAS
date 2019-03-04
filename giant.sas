libname sasdata "E:\SAS\SAS_Library";
libname db odbc noprompt="driver=SQL Server Native Client 11.0;
                          server=PARKSLAB;
                          database=HUMAN_GWAS;
                          Trusted_Connection=yes" schema=dbo;


data giant(keep = chr bp rsid beta p_value trait);
  infile "E:\John Li data\gwas-download-master\BMI\bmi_giant_ukbb_meta_analysis.txt"
        delimiter='09'x TRUNCOVER DSD firstobs=2;

  * read data in input order;
  input  chr$
         bp
         rsid$
         Tested_Allele
         Other_Allele 
         Freq_Tested_Allele
         beta SE p_value N INFO
	 ;

  trait  = 'giant';
run;


data ukbb_bmi(keep = chr bp rsid beta p_value trait);
 infile "E:\John Li data\gwas-download-master\BMI\BMI_UKBB"
        delimiter='09'x TRUNCOVER DSD firstobs=2;

  * read data in input order;
  input  variant$
         minor_allele
         minor_AF
         low_confidence_variant
         n_complete_samples
         AC ytx	beta se	tstat pval;

  chr    = scan(variant, 1, ':');
  bp     = input(scan(variant, 2, ':'), 32.);
  trait  = 'ukbb';
run;


data japanese(keep = chr bp beta p_value trait);
 infile "E:\John Li data\gwas-download-master\BMI\bmi_giant_ukbb_meta_analysis.txt"
        delimiter='09'x TRUNCOVER DSD firstobs=2;

  * read data in input order;
  input  SNP$
         chr$	bp
         REF	ALT	Frq	Rsq
         beta	SE	p_value
	 ;
	 
  trait  = 'japanese';
run;

data sasdata.bmi;
  set giant ukbb_bmi japanese;
run;


proc datasets library = db;
	append base = db.mvp_lipid data=sasdata.mvp_lipid;
run;
