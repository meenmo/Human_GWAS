libname sasdata "E:\SAS\SAS_Library";
libname db odbc noprompt="driver=SQL Server Native Client 11.0;
                          server=PARKSLAB;
                          database=HUMAN_GWAS;
                          Trusted_Connection=yes" schema=dbo;


data sasdata.giant(keep = chr bp rsid beta p_value trait);
  length snp$20;

/* delimter is a single space for this raw data, not a tab*/
  infile "E:\John Li data\gwas-download-master\BMI\bmi_giant_ukbb_meta_analysis.txt"
        dlm=' ' TRUNCOVER DSD firstobs=2;
 
/* read data in input order. Note that $ refers to character variables; without $ refers to numeric. */
  input  chr$
  	 bp
         SNP$
         Tested_Allele$
         Other_Allele $
         Freq_Tested_Allele
         beta SE p_value N INFO
	 ;

  rsid   = scan(SNP, 1, ':');
  trait  = 'giant';
run;




data sasdata.ukbb_bmi(keep = chr bp beta p_value trait);
 infile "E:\John Li data\gwas-download-master\BMI\BMI_UKBB.tsv"
        delimiter='09'x TRUNCOVER DSD firstobs=2;

  * read data in input order;
  input  variant$
         minor_allele$
         minor_AF
         low_confidence_variant$
         n_complete_samples
         AC ytx	beta se	tstat p_value;
  
/*Extract first value of delimited variable by : */
  chr    = scan(variant, 1, ':');
/* input converts the variable from characters to numeric. */
  bp     = input(scan(variant, 2, ':'),32.);
  trait  = 'ukbb';
run;


data sasdata.japanese(keep = chr bp beta p_value trait);
 infile "E:\John Li data\gwas-download-master\BMI\japanese_2017_BMI_BBJ_autosome.txt"
        delimiter='09'x TRUNCOVER DSD firstobs=2;

  * read data in input order;
  input  SNP$
         chr$	bp
         REF$	ALT$	Frq	Rsq
         beta	SE	p_value
	 ;
	 
  trait  = 'japanese';
run;



/* Push tables to SQL Server */
proc datasets library = db;
	append base = db.giant data=sasdata.giant;
run;

proc datasets library = db;
	append base = db.ukbb_bmi data=sasdata.ukbb_bmi;
run;

proc datasets library = db;
	append base = db.japanese data=sasdata.japanese;
run;