drop procedure cross_ref;

USE Human_GWAS
GO
CREATE PROCEDURE cross_ref @gene varchar(20), @margin float
  AS
  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start, b.bp, a.chr_end+@margin as adj_chr_end,
        b.chr, b.beta, b.p_value, b.trait
  FROM   [dbo].[hg19] as a,
        [dbo].[BMI_giant_bmi] as b
  WHERE  (a.gene_name = @gene) and (b.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start, c.bp, a.chr_end+@margin as adj_chr_end,
        c.chr, c.beta, c.p_value, c.trait
  FROM   [dbo].[hg19] as a,
        [dbo].[BMI_japanese_bmi] as c
  WHERE  (a.gene_name = @gene) and (c.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start, d.bp, a.chr_end+@margin as adj_chr_end,
        d.chr, d.beta, d.p_value, d.trait
  FROM   [dbo].[hg19] as a,
        [dbo].[BMI_ukbb_bmi_Neale] as d
  WHERE  (a.gene_name = @gene) and (d.bp between a.chr_start-@margin and a.chr_end+@margin)

                          UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start, e.bp, a.chr_end+@margin as adj_chr_end,
        e.chr, e.beta, e.p_value, e.trait
  FROM   [dbo].[hg19] as a,
        [dbo].[Lipid_Exome_Lu_East_Asian_NG] as e
  WHERE  (a.gene_name = @gene) and (e.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start, f.bp, a.chr_end+@margin as adj_chr_end,
        f.chr, f.beta, f.p_value, f.trait
  FROM   [dbo].[hg19] as a,
        [dbo].[Lipid_Exome_Lu_European_and_East_Asian_NG] as f
  WHERE  (a.gene_name = @gene) and (f.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start, g.bp, a.chr_end+@margin as adj_chr_end,
        g.chr, g.beta, g.p_value, g.trait
  FROM   [dbo].[hg19] as a,
        [dbo].[Lipid_GLGC_Exome_Liu_NG] as g
  WHERE  (a.gene_name = @gene) and (g.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

   
  --SELECT a.gene_name, a.chr_start-@margin as adj_chr_start,
  --                    h.bp,
  --                    a.chr_end +@margin as adj_chr_end,
  --       h.chr,h.beta,h.p_value,h.trait
  --FROM  [dbo].[hg19] as a,
  --      [dbo].[Lipid_GLGC_Willer_NG] as h
  --WHERE (a.gene_name = @gene) and (h.bp between a.chr_start-@margin and a.chr_end+@margin)

  --                       UNION

  --SELECT a.gene_name, a.chr_start-@margin as adj_chr_start,
  --                    j.bp,
  --                    a.chr_end  +@margin as adj_chr_end,
  --       j.chr,j.beta,j.p_value,j.trait
  --FROM   [dbo].[hg19] as a,
  --       [dbo].[Lipid_MVP_Klarin_NG] as j
  --WHERE  (a.gene_name = @gene) and (j.bp between a.chr_start-@margin and a.chr_end+@margin)

  --                       UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start,
                      k.bp,
                      a.chr_end  +@margin as adj_chr_end,
         k.chr,k.beta,k.p_value,k.trait
  FROM  [dbo].[hg19] as a,
        [dbo].[Lipid_prins_SCientific_REPORT] as k
  WHERE (a.gene_name = @gene) and (k.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start,
                      l.bp,
                      a.chr_end  +@margin as adj_chr_end,
        l.chr,l.beta, l.p_value,l.trait
  FROM  [dbo].[hg19] as a,
        [dbo].[Lipid_UKBB_lipid_trait_Neale] as l
  WHERE (a.gene_name = @gene) and (l.bp between a.chr_start-@margin and a.chr_end+@margin)

                         UNION

  SELECT a.gene_name, a.chr_start-@margin as adj_chr_start,
                      m.bp,
                      a.chr_end  +@margin as adj_chr_end,
         m.chr,m.beta,m.p_value,m.trait
  FROM   [dbo].[hg19] as a,
         [dbo].[Lipid_UKBB_statin_usage_Neale] as m
  WHERE  (a.gene_name = @gene) and (m.bp between a.chr_start-@margin and a.chr_end+@margin)

GO

EXEC cross_ref 'sesn1', 20000;
