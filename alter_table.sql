ALTER TABLE [dbo].[BMI_giant_bmi]
ALTER COLUMN table_name varchar(50)

ALTER TABLE [dbo].[BMI_giant_bmi]
	ADD DEFAULT 'BMI_giant_bmi' FOR table_name