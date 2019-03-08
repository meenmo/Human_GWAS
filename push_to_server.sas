libname sasdata "E:\SAS\SAS_Library";
libname db odbc noprompt="driver=SQL Server Native Client 11.0;
                          server=PARKSLAB;
                          database=HUMAN_GWAS;
                          Trusted_Connection=yes" readbuff = 32767 schema=dbo;


proc datasets library = db;
	append base = db.n_ukbb_bmi data=sasdata.ukbb_bmi;
	append base = db.n_Lipid_UKBB_lipid_trait data=sasdata.Lipid_UKBB_lipid_trait;
	append base = db.n_Lipid_UKBB_lipid_trait data=sasdata.Lipid_UKBB_lipid_trait;
run;
