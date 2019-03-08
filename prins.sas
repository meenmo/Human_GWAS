libname sasdata "e:\sas\sas_library";
libname db odbc noprompt="driver=SQL Server Native Client 11.0;
                          server=PARKSLAB;
                          database=HUMAN_GWAS;
                          Trusted_Connection=yes" readbuff = 32767 schema=dbo;


%macro prins(name, trait, path);
data prins_&name(keep=chr bp rsid beta p_value trait);
	length rsid $20 trait $3;
	infile &path dlm=' ' truncover dsd firstobs=1;

	input rsid$ 
		  chr$ 
		  bp 
		  a1$ a2$ 
		  p_value
		  beta
		  unknwon
		  ;
	
	trait = &trait;
run;
%mend prins;

%prins(chol, 'TC', "E:\John Li data\gwas-download-master\LIPID\prins\Prins_28887542_chol.txt")
%prins(hdl, 'HDL', "E:\John Li data\gwas-download-master\LIPID\prins\Prins_28887542_hdl.txt")
%prins(ldl, 'LDL', "E:\John Li data\gwas-download-master\LIPID\prins\Prins_28887542_ldl.txt")


data sasdata.prins;
	length chr $2;
	set prins_chol prins_hdl prins_ldl;
run;


proc sql;
	connect to odbc as db (required="driver sql server native client 11.0;
									 server=PARKSLAB;
									 Trusted_Connection=Yes;
									 Database=Human_GWAS;");

	execute(drop table prins) by db;
quit;


proc datasets library = db;
	append base = db.prins data = sasdata.prins;
run;
