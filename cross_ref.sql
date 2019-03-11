drop procedure cross_ref;

USE Human_GWAS
GO
CREATE PROCEDURE cross_ref @gene varchar(20), @margin numeric
	AS 
	SELECT hg19.chr_start, hg19.chr_end, hg19.gene_name,
		   [dbo].[BMI_giant_bmi].*,
		   [dbo].[BMI_japanese_bmi].*
		--,[dbo].[BMI_ukbb_bmi_Neale].*,
		 --[dbo].[Lipid_Exome_Lu_East_Asian_NG].*,
		 --[dbo].[Lipid_Exome_Lu_European_and_East_Asian_NG].*,
		 --[dbo].[Lipid_GLGC_Exome_Liu_NG].*,
		 --[dbo].[Lipid_GLGC_Willer_NG].*,
		 --[dbo].[Lipid_Japanese_lipid_trait_Kanai_NG].*,
		 --[dbo].[Lipid_MVP_Klarin_NG].*,
		 --[dbo].[Lipid_prins_SCientific_REPORT].*,
		 --[dbo].[Lipid_UKBB_lipid_trait_Neale].*,
		 --[dbo].[Lipid_UKBB_statin_usage_Neale].*

	FROM [dbo].[hg19],
		 [dbo].[BMI_giant_bmi],
		 [dbo].[BMI_japanese_bmi]
		 --,[dbo].[BMI_ukbb_bmi_Neale],
		 --[dbo].[Lipid_Exome_Lu_East_Asian_NG],
		 --[dbo].[Lipid_Exome_Lu_European_and_East_Asian_NG],
		 --[dbo].[Lipid_GLGC_Exome_Liu_NG],
		 --[dbo].[Lipid_GLGC_Willer_NG],
		 --[dbo].[Lipid_Japanese_lipid_trait_Kanai_NG],
		 --[dbo].[Lipid_MVP_Klarin_NG],
		 --[dbo].[Lipid_prins_SCientific_REPORT],
		 --[dbo].[Lipid_UKBB_lipid_trait_Neale],
		 --[dbo].[Lipid_UKBB_statin_usage_Neale]

	WHERE gene_name = @gene and
		  [dbo].[BMI_giant_bmi].bp between hg19.chr_start-@margin and hg19.chr_end+@margin and
		  [dbo].[BMI_japanese_bmi].bp between hg19.chr_start-@margin and hg19.chr_end+@margin and
	   --,[dbo].[BMI_ukbb_bmi_Neale].bp between hg19.chr_start-@margin and hg19.chr_end+@margin and,
		--[dbo].[Lipid_Exome_Lu_East_Asian_NG].bp between hg19.chr_start-@margin and hg19.chr_end+@margin and,
		--[dbo].[Lipid_Exome_Lu_European_and_East_Asian_NG].bp between hg19.chr_start-@margin and hg19.chr_end+@margin and,
		--[dbo].[Lipid_GLGC_Exome_Liu_NG].bp between hg19.chr_start-@margin and hg19.chr_end+@margin and,
		--[dbo].[Lipid_GLGC_Willer_NG].bp between hg19.chr_start-@margin and hg19.chr_end+@margin and,
		--[dbo].[Lipid_Japanese_lipid_trait_Kanai_NG].bp between hg19.chr_start-@margin and hg19.chr_end+@margin and,
		--[dbo].[Lipid_MVP_Klarin_NG].bp between hg19.chr_start-@margin and hg19.chr_end+@margin and,
		--[dbo].[Lipid_prins_SCientific_REPORT].bp between hg19.chr_start-@margin and hg19.chr_end+@margin and,
		--[dbo].[Lipid_UKBB_lipid_trait_Neale].bp between hg19.chr_start-@margin and hg19.chr_end+@margin and,
		--[dbo].[Lipid_UKBB_statin_usage_Neale].bp between hg19.chr_start-@margin and hg19.chr_end+@margin 

GO

EXEC cross_ref 'sesn1', 20000;
