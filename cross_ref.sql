-- drop procedure cross_ref;

USE Human_GWAS
GO
CREATE PROCEDURE cross_ref @gene varchar(20), @margin numeric
  AS

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start, b.bp, a.chr_end+@margin as adj_chr_end,
         b.chr, b.beta, b.p_value, b.trait,
         'lipid_japanese' as TableName
  FROM   [dbo].[hg19] as a,
         [dbo].[Lipid_Japanese_lipid_trait_Kanai_NG] as b
  WHERE  (a.gene_name = @gene) and (a.chr = b.chr) and (b.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start, b.bp, a.chr_end+@margin as adj_chr_end,
         b.chr, b.beta, b.p_value, b.trait,
         'BMI_giant_bmi' as TableName

  FROM  [dbo].[hg19] as a,
        [dbo].[BMI_giant_bmi] as b
  WHERE (a.gene_name = @gene) and (a.chr = b.chr) and (b.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start, c.bp, a.chr_end+@margin as adj_chr_end,
         c.chr, c.beta, c.p_value, c.trait,
         'BMI_japanese_bmi' as TableName
  FROM   [dbo].[hg19] as a,
         [dbo].[BMI_japanese_bmi] as c
  WHERE  (a.gene_name = @gene) and (a.chr = c.chr) and (c.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start, d.bp, a.chr_end+@margin as adj_chr_end,
         d.chr, d.beta, d.p_value, d.trait,
         'BMI_ukbb_bmi_Neale' as TableName
  FROM   [dbo].[hg19] as a,
         [dbo].[BMI_ukbb_bmi_Neale] as d
  WHERE  (a.gene_name = @gene) and (a.chr = d.chr) and (d.bp between a.chr_start-@margin and a.chr_end+@margin)

                          UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start, e.bp, a.chr_end+@margin as adj_chr_end,
         e.chr, e.beta, e.p_value, e.trait,
         'Lipid_Exome_Lu_East_Asian' as TableName
  FROM   [dbo].[hg19] as a,
         [dbo].[Lipid_Exome_Lu_East_Asian_NG] as e
  WHERE  (a.gene_name = @gene) and  (a.chr = e.chr) and (e.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start, f.bp, a.chr_end+@margin as adj_chr_end,
         f.chr, f.beta, f.p_value, f.trait,
         'Lipid_Exome_Lu_European_and_East_Asian' as TableName
  FROM   [dbo].[hg19] as a,
         [dbo].[Lipid_Exome_Lu_European_and_East_Asian_NG] as f
  WHERE  (a.gene_name = @gene) and (a.chr = f.chr) and (f.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start, g.bp, a.chr_end+@margin as adj_chr_end,
         g.chr, g.beta, g.p_value, g.trait,
         'Lipid_GLGC_Exome_Liu_NG' as g
  FROM   [dbo].[hg19] as a,
         [dbo].[Lipid_GLGC_Exome_Liu_NG] as g
  WHERE  (a.gene_name = @gene) and  (a.chr = g.chr) and (g.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start,
         h.bp, a.chr_end +@margin as adj_chr_end,
         h.chr,h.beta,h.p_value,h.trait,
        'Lipid_GLGC_Willer' as TableName
  FROM  [dbo].[hg19] as a,
        [dbo].[Lipid_GLGC_Willer_NG] as h
  WHERE (a.gene_name = @gene) and (a.chr = h.chr) and (h.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start,
         j.bp,a.chr_end  +@margin as adj_chr_end,
         j.chr,j.beta,j.p_value,j.trait,
  			 'Lipid_MVP_Klarin_NG' as TableName
  FROM   [dbo].[hg19] as a,
         [dbo].[Lipid_MVP_Klarin_NG] as j
  WHERE  (a.gene_name = @gene) and (a.chr = j.chr) and (j.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start,
         k.bp,a.chr_end  +@margin as adj_chr_end,
         k.chr,k.beta,k.p_value,k.trait,
  			 'Lipid_prins_SCientific_REPORT' as TableName
  FROM   [dbo].[hg19] as a,
         [dbo].[Lipid_prins_SCientific_REPORT] as k
  WHERE  (a.gene_name = @gene) and (a.chr = k.chr) and (k.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start,
         l.bp,a.chr_end  +@margin as adj_chr_end,
         l.chr,l.beta, l.p_value,l.trait,
  			 'Lipid_UKBB_lipid_trait' as TableName
  FROM   [dbo].[hg19] as a,
         [dbo].[Lipid_UKBB_lipid_trait_Neale] as l
  WHERE  (a.gene_name = @gene) and (a.chr = l.chr) and (l.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start,
         m.bp,a.chr_end  +@margin as adj_chr_end,
         m.chr,m.beta,m.p_value,m.trait,
         'Lipid_UKBB_statin_usage' as TableName
  FROM   [dbo].[hg19] as a,
         [dbo].[Lipid_UKBB_statin_usage_Neale] as m
  WHERE  (a.gene_name = @gene) and (a.chr = m.chr) and (m.bp between a.chr_start-@margin and a.chr_end+@margin)

                           UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start,
         n.bp,a.chr_end  +@margin as adj_chr_end,
         n.chr,n.beta,n.p_value,n.trait,
		     'Japanese_lipid_Trait' as TableName
  FROM   [dbo].[hg19] as a,
         [dbo].[Lipid_Japanese_lipid_trait_Kanai_NG]as n
  WHERE  (a.gene_name = @gene) and (a.chr = n.chr) and (n.bp between a.chr_start-@margin and a.chr_end+@margin)
