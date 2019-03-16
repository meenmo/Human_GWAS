libname sasdata "E:\SAS\SAS_Library";
libname db odbc noprompt="driver=SQL Server Native Client 11.0;
                          server=PARKSLAB;
                          database=HUMAN_GWAS;
                          Trusted_Connection=yes" schema=dbo;


data sasdata.giant(keep = chr bp rsid beta p_value trait);
	length chr$2 snp$20;

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
	/*Load raw data
	 delimiter='09'x is for tab-delimited file
	 Truncover foces the INPUT statement to stop reading when it gets to the end of a short line.
	 DSD considers an observation a missing value if there are two delimiters in a row
	 The first line will be read from the second line of the raw data since the first line will be column names */
	
	infile "E:\John Li data\gwas-download-master\BMI\BMI_UKBB.tsv" delimiter='09'x TRUNCOVER DSD firstobs=2;

	/*Read data in input order
	  Followings will be each name of a column for raw data
	  Input name followed by dollar sign($) is to specify that type of the column is character
	  Column without $ is numeric/float */
	  
	input  variant$
	       minor_allele$
	       minor_AF
	       low_confidence_variant$
	       n_complete_samples
	       AC ytx beta se tstat p_value;


	/*This is to seprate values individually within a column delimited by colon; e.g.) 5:12345:abc:a12
	  So the line below is to extract first value of delimited variable by : 
	  
	  variant is column name as specified above under input statement
	  1 refers to the first value of the corresponding string; this will be 5 for the example of 5:12345:abc:a12
	  I am not converting this to be numeric since character value could be included into this column like 'X' */
	
	chr    = scan(variant, 1, ':');
	
	/*This is for the second value of the string. The column 'variant' is read as character, but this is value is numeric. 
	  Hence, we need to convert this column 'bp' into numeric using 'input'.
	  32. is a format for numeric*/
	  
	bp     = input(scan(variant, 2, ':'),32.);
	
	/*We are adding a column 'trait' and all observations of this column are set to be 'ukbb'. */
	trait  = 'ukbb';
run;


data sasdata.japanese(keep = chr bp beta p_value trait);
	infile "E:\John Li data\gwas-download-master\BMI\japanese_2017_BMI_BBJ_autosome.txt"
		delimiter='09'x TRUNCOVER DSD firstobs=2;

	/* read data in input order */	
	input  SNP$
	       chr$	bp
	       REF$	ALT$	Frq	Rsq
	       beta	SE	p_value
	       ;

	trait  = 'japanese';
	
run;


proc datasets library = db;
	append base = db.giant	  data = sasdata.giant;
	append base = db.ukbb_bmi data = sasdata.ukbb_bmi;
	append base = db.japanese data = sasdata.japanese;
run;
