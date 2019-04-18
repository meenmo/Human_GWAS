libname db odbc noprompt="driver=SQL Server Native Client 11.0;
                          server=PARKSLAB;
                          database=HUMAN_GWAS;
                          Trusted_Connection=yes" SCHEMA=dbo;


data hg19_snp;
	infile "E:\John Li data\hg\hg19_snp.txt" delimiter='09'x truncover dsd firstobs=2;
	input chr$ strt ed rsid$;
	
	chr = compress(chr,'chr');
	if chr ^= '6' then delete;
run;


data data01;
	infile "E:\John Li data\hg\data01.txt" delimiter=',' truncover dsd firstobs=2;
	input id chr$ bp MAF p_values beta varbeta;
run;

data data02;
	infile "E:\John Li data\hg\data02.txt" delimiter=',' truncover dsd firstobs=2;
	input id chr$ bp MAF p_values beta varbeta;
run;

data data03;
	infile "E:\John Li data\hg\data03.txt" delimiter=',' truncover dsd firstobs=2;
	input id chr$ bp MAF p_values beta varbeta;
run;


proc datasets library = db;
	append base = db.hg19_snp data=work.hg19_snp;
	append base = db.data01 data=work.data01;
	append base = db.data02 data=work.data02;
	append base = db.data03 data=work.data03;
run;



/*select a.id, a.chr, b.strt, a.bp, b.ed, a.maf, a.p_values, a.beta, a.varbeta, b.rsid*/
/**/
/*from [dbo].[data01] as a*/
/*left join [dbo].[hg19_snp] as b */
/*on a.bp between b.strt and b.ed;*/
