libname sasdata "e:\sas\sas_library";

data hg19_snp;
	infile "E:\John Li data\hg\hg19_snp.txt" delimiter='09'x truncover dsd firstobs=2;
	input chr$ start end rsid$;
	
	chr = compress(chr,'chr');
	if chr ^= '6' then delete;
run;

proc sort data=hg19_snp;
	by start;
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



/*data data01_s;*/
/*	set data01(obs=100);*/
/*run;*/

proc sql;
	create table sasdata.data01_snp as
	select a.id, a.chr, b.start, a.bp, b.end, a.maf, a.p_values, a.beta, a.varbeta, b.rsid
	from data01 a 
	left join hg19_snp b 
	on b.start <= a.bp <= b.end
	order by id;
quit;

proc sql;
	create table sasdata.data02_snp as
	select a.id, a.chr, b.start, a.bp, b.end, a.maf, a.p_values, a.beta, a.varbeta, b.rsid
	from data02 a 
	left join hg19_snp b 
	on b.start <= a.bp <= b.end
	order by id;
quit;


proc sql;
	create table sasdata.data03_snp as
	select a.id, a.chr, b.start, a.bp, b.end, a.maf, a.p_values, a.beta, a.varbeta, b.rsid
	from data03 a 
	left join hg19_snp b 
	on b.start <= a.bp <= b.end
	order by id;
quit;
