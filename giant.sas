libname sasdata "E:\SAS\SAS_Library";

data giant(keep = chr bp rsid beta p_value trait);
  infile "E:\John Li data\gwas-download-master\BMI\bmi_giant_ukbb_meta_analysis.txt"
        delimiter='09'x TRUNCOVER DSD firstobs=2;

  %* set length and informat and output order;
  informat chr $2.
    		   bp 8.
           rsid $10.
           beta p_value 8.
    		   trait $8.;

  %* read data in input order;
  input  chr
         bp
         rsid
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

  %* set length and informat and output order;
  informat chr $2.
    		   bp 8.
           rsid $10.
           beta p_value 8.
    		   trait $8.;

  %* read data in input order;
  input  variant
         minor_allele
         minor_AF
         low_confidence_variant
         n_complete_samples
         AC	ytx	beta	se	tstat	pval;

  chr    = scan(variant, 1, ':');
  bp     = scan(variant, 2, ':');
  rsid   = ''
  trait  = 'ukbb';
run;


data japanese(keep = chr bp beta p_value trait);
 infile "E:\John Li data\gwas-download-master\BMI\bmi_giant_ukbb_meta_analysis.txt"
        delimiter='09'x TRUNCOVER DSD firstobs=2;

  %* set length and informat and output order;
  informat chr $2.
    		   bp 8.
           rsid $10.
           beta p_value 8.
    		   trait $8.;

  %* read data in input order;
  input  SNP
         chr	bp
         REF	ALT	Frq	Rsq
         beta	SE	p_value
		     ;
  rsid   = ''
  trait  = 'japanese';
run;

data sasdata.bmi;
  set giant ukbb_bmi japanese;
run;


proc sql;
   connect to odbc as db (required="driver=sql server native client 11.0;
                							 	    seerver=PARKSLAB;
                								    Trusted_Connection=Yes;
                								    Database=Human_GWAS;");

	execute(drop table mvp_lipid) by db;
	execute(create table mvp_lipid (
  		    chr     varchar(2),
  		    bp      numeric(18),
          rsid    varchar(10),
  		    beta    float,
  		    p_value float,
  		    trait   varchar(8)
			    )) by db;
quit;


libname db odbc noprompt = "server=PARKSLAB;DRIVER=SQL Server Native Client 11.0;
							  Trusted_Connection=yes" DATABASE = Human_GWAS schema = dbo;

proc datasets library = db;
	append base = db.mvp_lipid data=sasdata.mvp_lipid;
run;
