libname sasdata "E:\SAS\SAS_Library";
libname db odbc noprompt="driver=SQL Server Native Client 11.0;
                          server=PARKSLAB;
                          database=HUMAN_GWAS;
                          Trusted_Connection=yes" schema=dbo;

%macro cleanup_raw(path, dataset, trait);
data &dataset (keep = rsid beta p_value trait chr bp);

	/* These two variables are truncated; so I specify their length */
	length SNP_hg19 rsid$20;
	
	/*'09'x for tab delimited */
	infile &path delimiter='09'x TRUNCOVER DSD firstobs=2;

	* read data in input order;
	input    SNP_hg18$
		 SNP_hg19$
		 rsid$
		 A1$ A2$
		 beta se N p_value Freq_A1_1000G_EUR
		 ;

	trait = &trait;
	
	/* the raw data looks like chr10; remove chr at the front. */
	chr = compress(scan(snp_hg19, 1, ':'),'chr');
	bp  = input(scan(snp_hg19, 2, ':'),32.);

run;
%mend cleanup_raw;

%cleanup_raw("E:\HUMAN_GWAS_GLGC_DATA\jointGwasMc_HDL.txt", HDL, 'HDL')
%cleanup_raw("E:\HUMAN_GWAS_GLGC_DATA\jointGwasMc_LDL.txt", LDL, 'LDL')
%cleanup_raw("E:\HUMAN_GWAS_GLGC_DATA\jointGwasMc_TC.txt", TC, 'TC')
%cleanup_raw("E:\HUMAN_GWAS_GLGC_DATA\jointGwasMc_TG.txt", TG, 'TG')

/* merge four tables into a single table; remove unnecessary lenght for chr */
data sasdata.GLGC;
	length chr $2;
	set HDL LDL TC TG;
run;

/* drop existing table in sql server if necessary */
proc sql;
	connect to odbc as db (required="driver=sql server native client 11.0;
					 seerver=PARKSLAB;
					 Trusted_Connection=Yes;
					 Database=Human_GWAS;");
	execute(drop table glgc) by db;
quit;

/* push table to sql server */
proc datasets library = db;
	append base = db.GLGC data=sasdata.GLGC;
run;
