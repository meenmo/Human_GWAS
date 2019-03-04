libname sasdata "E:\SAS\SAS_Library";

/*proc sql;*/
/*	connect to odbc (required="driver=sql server native client 11.0;*/
/*					 		   seerver=PARKSLAB;*/
/*							   Trusted_Connection=Yes;*/
/*							   Database=Human_GWAS;");*/

%macro ukbb(dataset, trait, path);
data &dataset(keep = chr bp beta pval trait);
 infile &path	delimiter='09'x TRUNCOVER DSD firstobs=2;

  %* set length and informat and output order;
  informat chr $5.
		   bp  8.
           MUTANT ORIG $70.
           MINOR_ALLELE $2.
           MINOR_AF EXPECTED_CASE_MINOR_AC 8.
           LOW_CONFIDENCE_VARIANT  $5.
           N_COMPLETE_SAMPLES AC YTX beta SE TSTAT PVAL 8.
           VARIANT $70.
		   trait $20.;

  %* read data in input order;
  input  VARIANT 
		 MINOR_ALLELE 
		 MINOR_AF
         EXPECTED_CASE_MINOR_AC 
		 LOW_CONFIDENCE_VARIANT
         N_COMPLETE_SAMPLES  
         AC YTX ( beta SE TSTAT PVAL ) (:?? 32.) ;

  drop VARIANT ;

  chr    = scan(VARIANT, 1,':');
  bp     = input(scan(VARIANT, 2,':'),?? 32.);
  trait  = &trait;
run;
%mend ukbb;


%ukbb(medicat,'statin_usage',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\cholesterol_lower_medication.tsv")
%ukbb(male,'self_reported_high_cholesterol_male',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\self_reported_highcholesterol_male.tsv")
%ukbb(female,'self_reported_high_cholesterol_female',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\self_reported_high_cholesterol_female.tsv")
%ukbb(both,'self_reported_high_cholesterol_both',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\selfreported_high_cholesterol_both_sexes.tsv")

data sasdata.ukbb_statin(rename = (PVAL=p_value));
	set atorvastatin rosuvastatin pravastatin fluvastatin sivastatin;
run;

%ukbb(atorvastatin,'atorvastatin',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\atorvastatin.both_sexes.tsv")
%ukbb(rosuvastatin,'rosuvastatin',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\rosuvastatin.both_sexes.tsv")
%ukbb(pravastatin, 'pravastatin',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\pravastatin_both_sexes.tsv")
%ukbb(fluvastatin, 'fluvastatin',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\fluvastatin.both_sexes.tsv")
%ukbb(sivastatin,  'sivastatin',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\sivastatin_both_sexes.tsv")

data sasdata.ukbb_statin(rename = (PVAL=p_value));
	set atorvastatin rosuvastatin pravastatin fluvastatin sivastatin;
run;


proc sql;
   connect to odbc as db (required="driver=sql server native client 11.0;
							 	    seerver=PARKSLAB;
								    Trusted_Connection=Yes;
								    Database=Human_GWAS;");

	execute(drop table ukbb_statin) by db;
	execute(create table ukbb_statin (
		    chr varchar(2),
		    bp numeric(18),
		    beta float,
		    p_value float,
		    trait varchar(20) 
			)) by db;
	execute(insert into ukbb_statin
										) by db;
quit;



libname db odbc noprompt = "server=PARKSLAB;DRIVER=SQL Server Native Client 11.0;						  
							  Trusted_Connection=yes" DATABASE = Human_GWAS libname schema = dbo;;

proc datasets library = db;
	append base = db.ukbb_statin data=sasdata.ukbb_statin;
run;

