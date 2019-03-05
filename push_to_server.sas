libname sasdata "E:\SAS\SAS_Library";
libname db odbc noprompt="driver=SQL Server Native Client 11.0;
                          server=PARKSLAB;
                          database=HUMAN_GWAS;
                          Trusted_Connection=yes" schema=dbo;


%macro push(t1, t2, t3, t4, t5, t6, t7, t8, t9);
<<<<<<< HEAD
/* drop existing table in sql server if necessary */
/*proc sql;*/
/*	connect to odbc as db (required="driver=sql server native client 11.0;*/
/*									 seerver=PARKSLAB;*/
/*									 Trusted_Connection=Yes;*/
/*									 Database=Human_GWAS;");*/
/**/
/*  	execute(drop table &t1) by db;*/
/*    execute(drop table &t2) by db;*/
/*    execute(drop table &t3) by db;*/
/*    execute(drop table &t4) by db;*/
/*    execute(drop table &t5) by db;*/
/*    execute(drop table &t6) by db;*/
/*    execute(drop table &t7) by db;*/
/*    execute(drop table &t8) by db;*/
/*    execute(drop table &t9) by db;*/
/*  quit;*/

=======

/* drop existing tables in the server */
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
>>>>>>> 59144f5b422f08725464d57f70ec9007ccab754b

/* push table to sql server */
proc datasets library = db;
	append base = db.n_&t1 data=sasdata.&t1;
	append base = db.n_&t2 data=sasdata.&t2;
	append base = db.n_&t3 data=sasdata.&t3;
	append base = db.n_&t4 data=sasdata.&t4;
	append base = db.n_&t5 data=sasdata.&t5;
	append base = db.n_&t6 data=sasdata.&t6;
	append base = db.n_&t7 data=sasdata.&t7;
	append base = db.n_&t8 data=sasdata.&t8;
	append base = db.n_&t9 data=sasdata.&t9;
run;

%mend push;



proc printto log='E:\SAS\server.log';
run;
%push(mvp_lipid,
	  East_Asian,
      European,
	  giant,
	  japanese,
	  glgc,
	  ukbb_bmi,
	  Lipid_UKBB_lipid_trait,
      Lipid_ukbb_statin_usage
      )
proc printto;
run;
