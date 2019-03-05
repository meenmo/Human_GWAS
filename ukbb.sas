libname sasdata "E:\SAS\SAS_Library";

%macro ukbb(dataset, trait, path);
	data &dataset(keep = chr bp beta p_valUE trait);

	length variant $100;

	infile &path delimiter='09'x TRUNCOVER DSD firstobs=2;

	* read data in input order;
	input    variant $
		 minor_allele $
		 minor_AF
		 expected_case_minor_AC
		 low_confidence_variant	$
		 n_complete_samples
		 AC
		 ytx
		 beta
		 se
		 tstat
		 p_value
		 ;

	chr    = scan(VARIANT, 1,':');
	bp     = input(scan(VARIANT, 2,':'), 32.);
	trait  = &trait;

run;
%mend ukbb;


%ukbb(medicat,'statin_usage',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\cholesterol_lower_medication.tsv")
%ukbb(male,'self_reported_high_cholesterol_male',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\self_reported_highcholesterol_male.tsv")
%ukbb(female,'self_reported_high_cholesterol_female',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\self_reported_high_cholesterol_female.tsv")
%ukbb(both,'self_reported_high_cholesterol_both',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\selfreported_high_cholesterol_both_sexes.tsv")

data sasdata.Lipid_UKBB_lipid_trait;
	length chr$2;
	set medicat male female both;
run;


%ukbb(atorvastatin,'atorvastatin',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\atorvastatin.both_sexes.tsv")
%ukbb(rosuvastatin,'rosuvastatin',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\rosuvastatin.both_sexes.tsv")
%ukbb(pravastatin, 'pravastatin',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\pravastatin_both_sexes.tsv")
%ukbb(fluvastatin, 'fluvastatin',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\fluvastatin.both_sexes.tsv")
%ukbb(sivastatin,  'sivastatin',"E:\John Li data\gwas-download-master\UKBB_lipid_and_statin_neile_lab\sivastatin_both_sexes.tsv")

data sasdata.Lipid_ukbb_statin_usage;
	length chr$2;
	set atorvastatin rosuvastatin pravastatin fluvastatin sivastatin;
run;
