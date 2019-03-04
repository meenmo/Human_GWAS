libname sasdata "E:\SAS\SAS_Library";
libname db odbc noprompt="driver=SQL Server Native Client 11.0;
                          server=PARKSLAB;
                          database=HUMAN_GWAS;
                          Trusted_Connection=yes" schema=dbo;

%macro push(t1, t2, t3, t4, t5, t6, t7, t8, t9);
/* drop existing table in sql server if necessary */
proc sql;
	connect to odbc as db (required="driver=sql server native client 11.0;
									 seerver=PARKSLAB;
									 Trusted_Connection=Yes;
									 Database=Human_GWAS;");

  	execute(drop table &t1) by db;
    execute(drop table &t2) by db;
    execute(drop table &t3) by db;
    execute(drop table &t4) by db;
    execute(drop table &t5) by db;
    execute(drop table &t6) by db;
    execute(drop table &t7) by db;
    execute(drop table &t8) by db;
    execute(drop table &t9) by db;
  quit;


/* push table to sql server */
proc datasets library = db;
	append base = db.&t1 data=sasdata.&t1;
	append base = db.&t2 data=sasdata.&t2;
	append base = db.&t3 data=sasdata.&t3;
	append base = db.&t4 data=sasdata.&t4;
	append base = db.&t5 data=sasdata.&t5;
	append base = db.&t6 data=sasdata.&t6;
	append base = db.&t7 data=sasdata.&t7;
	append base = db.&t8 data=sasdata.&t8;
	append base = db.&t9 data=sasdata.&t9;
run;
%mend push;


%push(Lipid_UKBB_lipid_trait,
      Lipid_ukbb_statin_usage,
      East_Asian,
      mvp_lipid,
      European,
      giant,
      ukbb_bmi,
      japanese,
      glgc)
