--drop procedure cross_ref;

USE Human_GWAS
GO
CREATE PROCEDURE cross_ref @gene varchar(20), @margin numeric
	AS 
	SELECT a.chr_start, a.chr_end, a.gene_name,
	       b.*,
	       c.*,
	       d.*,
	       e.*,
	       f.*,
	       g.*,
	       h.*,
	       i.*,
	       j.*,
	       k.*,
	       l.*,
	       m.*
		   

	FROM   [dbo].[hg19] as a,
	       [dbo].[BMI_giant_bmi] as b,
	       [dbo].[BMI_japanese_bmi] as c,
	       [dbo].[BMI_ukbb_bmi_Neale] as d,
	       [dbo].[Lipid_Exome_Lu_East_Asian_NG] as e,
	       [dbo].[Lipid_Exome_Lu_European_and_East_Asian_NG] as f,
	       [dbo].[Lipid_GLGC_Exome_Liu_NG] as g,
	       [dbo].[Lipid_GLGC_Willer_NG] as h,
	       [dbo].[Lipid_Japanese_lipid_trait_Kanai_NG] as i,
	       [dbo].[Lipid_MVP_Klarin_NG] as j,
	       [dbo].[Lipid_prins_SCientific_REPORT] as k,
	       [dbo].[Lipid_UKBB_lipid_trait_Neale] as l,
	       [dbo].[Lipid_UKBB_statin_usage_Neale] as m
 
	WHERE  gene_name = @gene and
	       b.bp between a.chr_start-@margin and a.chr_end+@margin or
	       c.bp between a.chr_start-@margin and a.chr_end+@margin or
	       d.bp between a.chr_start-@margin and a.chr_end+@margin or
	       e.bp between a.chr_start-@margin and a.chr_end+@margin or
	       f.bp between a.chr_start-@margin and a.chr_end+@margin or
	       g.bp between a.chr_start-@margin and a.chr_end+@margin or	
	       h.bp between a.chr_start-@margin and a.chr_end+@margin or
	       i.bp between a.chr_start-@margin and a.chr_end+@margin or
	       j.bp between a.chr_start-@margin and a.chr_end+@margin or
	       k.bp between a.chr_start-@margin and a.chr_end+@margin or
	       l.bp between a.chr_start-@margin and a.chr_end+@margin or
	       m.bp between a.chr_start-@margin and a.chr_end+@margin

GO

--EXEC cross_ref 'sesn1', 20000;
