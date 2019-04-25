libname db odbc noprompt="driver=SQL Server Native Client 11.0;
                          server=PARKSLAB;
                          database=HUMAN_GWAS;
                          Trusted_Connection=yes" schema=dbo;

data liver(drop = id);
	length gene_id$20;

	infile "E:\John Li data\hg\0-eqtl_liver_sesn1.txt"
	dlm=',' TRUNCOVER DSD firstobs=2;

	input id
		  gene_id$
		  chr$
		  bp_hg19
		  ori$ mut$ b3$ 
		  distance$
		  m1 m2 maf pvalues slope slopese type$ s$ N;
run;

proc datasets library = db;
	append base = db.eqtl_liver_sesn1 data=work.liver;
run;
