data hg19_snp;
	infile "E:\John Li data\hg\hg19_snp.txt" delimiter='09'x truncover dsd firstobs=2;
	input chr$ start end rsid$;

	chr = compress(chr,'chr');
run;


/*proc sql;*/
/*	create table snp as*/
/*	select chr, min(start) as start, max(end) as end, rsid*/
/*	from hg19_snp*/
/*	group by rsid;*/
/*quit;*/


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
	create table data01_snp as
	select a.id, a.chr, b.start, a.bp, b.end, a.maf, a.p_values, a.beta, a.varbeta, b.rsid
	from data01(obs=1000) a 
	left join hg19_snp b 
	on a.chr=b.chr and b.start <= a.bp <= b.end
	order by id;
quit;

proc sql;
	create table data02_snp as
	select a.id, a.chr, b.start, a.bp, b.end, a.maf, a.p_values, a.beta, a.varbeta, b.rsid
	from data02(obs=100) a 
	left join hg19_snp b 
	on a.chr=b.chr and b.start <= a.bp <= b.end
	order by id;
quit;




proc sql;
	create table data03_snp as
	select a.id, a.chr, b.start, a.bp, b.end, a.maf, a.p_values, a.beta, a.varbeta, b.rsid
	from data03(obs=100) a 
	left join hg19_snp b 
	on a.chr=b.chr and b.start <= a.bp <= b.end
	order by id;
quit;
