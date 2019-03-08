drop procedure cross_ref;

USE Human_GWAS
GO
CREATE PROCEDURE cross_ref @gene varchar(20), @margin numeric
AS 
SELECT hg19.chr_start, hg19.chr_end, BMI_giant_bmi.*,[dbo].[Lipid_Exome_Lu_East_Asian_NG].*
FROM hg19, BMI_giant_bmi, [dbo].[Lipid_Exome_Lu_East_Asian_NG]
WHERE gene_name = @gene and
	  BMI_giant_bmi.bp between hg19.chr_start-@margin and hg19.chr_end+@margin
GO

EXEC cross_ref 'sesn1', 20000;