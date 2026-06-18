* ===================================================================.
* BI and Decision-Making Quality in SMEs - SPSS analysis (n = 178).
* Source: Google Form export of 188 valid responses; 1 removed for
* contradictory consent and 9 for careless responding (identical answer
* to all 17 items) -> n = 178. No missing data; all items in range.
* Output is the document of record. Validity analyses SPSS cannot do
* (CFA, HTMT, AVE/CR, Fornell-Larcker) are in BI_DMQ_validity.py.
* ===================================================================.
* Coding: Company_Size 1=<50 2=50-99 3=99-250(medium).
*         Job_Position 1=CEO 2=Senior 3=Middle 4=Operational 5=Other.
*         Industry 1=Manufacturing 2=Retail 3=Service 4=Technology 5=Other.
*         Items: 1=Strongly Disagree ... 5=Strongly Agree.
* ===================================================================.

* IMPORT (edit the path to your machine; or File > Import Data > CSV).
GET DATA /TYPE=TXT
  /FILE="BI_DMQ_data_coded_n178_SPSS_ready_ID_preserved.csv"
  /DELIMITERS="," /QUALIFIER='"' /FIRSTCASE=2
  /VARIABLES=
    ID F6.2
    Company_Size F1.0 Job_Position F1.0 Industry F1.0
    Strategic_BI_Availability F1.0 Strategic_BI_Alternatives F1.0 Strategic_BI_Alignment F1.0
    Tactical_BI_Availability F1.0 Tactical_BI_Resource_Alloc F1.0 Tactical_BI_Data_Decisions F1.0
    Operational_BI_Availability F1.0 Operational_BI_Agility F1.0 Operational_BI_Quality F1.0
    BI_Improves_Decisions F1.0 BI_Speed_Accuracy F1.0 BI_Data_Inform F1.0 BI_Alternative_Solutions F1.0
    BI_Cost_Barrier F1.0 BI_Training_Limit F1.0 BI_Flexibility_Issue F1.0 BI_Data_Integration_Issue F1.0.
DATASET NAME DataSet178 WINDOW=FRONT.
VALUE LABELS Company_Size 1 '<50' 2 '50-99' 3 '99-250'.
VALUE LABELS Job_Position 1 'CEO' 2 'Senior Manager' 3 'Middle Manager' 4 'Operational Manager' 5 'Other'.
VALUE LABELS Industry 1 'Manufacturing' 2 'Retail' 3 'Service' 4 'Technology' 5 'Other'.

COMPUTE Strategic_Mean   = MEAN(Strategic_BI_Availability,Strategic_BI_Alternatives,Strategic_BI_Alignment).
COMPUTE Tactical_Mean    = MEAN(Tactical_BI_Availability,Tactical_BI_Resource_Alloc,Tactical_BI_Data_Decisions).
COMPUTE Operational_Mean = MEAN(Operational_BI_Availability,Operational_BI_Agility,Operational_BI_Quality).
COMPUTE Decision_Making_Quality = MEAN(BI_Improves_Decisions,BI_Speed_Accuracy,BI_Data_Inform,BI_Alternative_Solutions).
EXECUTE.

* ===== STEP A0: data screening (range + univariate outliers). =======.
* (protocol items 3-4: z-scores beyond +/-3.29 flag univariate outliers).
DESCRIPTIVES VARIABLES=Strategic_Mean Tactical_Mean Operational_Mean Decision_Making_Quality
  /SAVE /STATISTICS=MEAN STDDEV MIN MAX.

* ===== STEP 0: demographics incl. firm size (Table 1). ==============.
FREQUENCIES VARIABLES=Company_Size Job_Position Industry.

* ===== STEP 1: reliability + item-total + alpha-if-deleted. =========.
RELIABILITY VARIABLES=Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
  /SCALE('Strategic BI') ALL /MODEL=ALPHA /SUMMARY=TOTAL.
RELIABILITY VARIABLES=Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
  /SCALE('Tactical BI') ALL /MODEL=ALPHA /SUMMARY=TOTAL.
RELIABILITY VARIABLES=Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
  /SCALE('Operational BI') ALL /MODEL=ALPHA /SUMMARY=TOTAL.
RELIABILITY VARIABLES=BI_Improves_Decisions BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /SCALE('DMQ') ALL /MODEL=ALPHA /SUMMARY=TOTAL.
RELIABILITY VARIABLES=BI_Training_Limit BI_Cost_Barrier BI_Data_Integration_Issue BI_Flexibility_Issue
  /SCALE('Challenges') ALL /MODEL=ALPHA /SUMMARY=TOTAL.

* ===== STEP 2: factorability + EFA + SAVE factor scores. ============.
* KMO, Bartlett, communalities, loadings, % variance; saves Strategic1 etc.
FACTOR VARIABLES=Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
  /PRINT=KMO EXTRACTION /CRITERIA=FACTORS(1) /EXTRACTION=PAF /ROTATION=NOROTATE /SAVE REG(ALL Strategic).
FACTOR VARIABLES=Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
  /PRINT=KMO EXTRACTION /CRITERIA=FACTORS(1) /EXTRACTION=PAF /ROTATION=NOROTATE /SAVE REG(ALL Tactical).
FACTOR VARIABLES=Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
  /PRINT=KMO EXTRACTION /CRITERIA=FACTORS(1) /EXTRACTION=PAF /ROTATION=NOROTATE /SAVE REG(ALL Operational).
FACTOR VARIABLES=BI_Improves_Decisions BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /PRINT=KMO EXTRACTION /CRITERIA=FACTORS(1) /EXTRACTION=PAF /ROTATION=NOROTATE /SAVE REG(ALL DMQ).

* ===== STEP 3: Harman single-factor (CMB). =========================.
FACTOR VARIABLES=Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
  Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
  Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
  BI_Improves_Decisions BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /PRINT=EXTRACTION /CRITERIA=FACTORS(1) /EXTRACTION=PAF /ROTATION=NOROTATE.

* ===== STEP 4: descriptives + formal normality test. ===============.
DESCRIPTIVES VARIABLES=Strategic_Mean Tactical_Mean Operational_Mean Decision_Making_Quality
  /STATISTICS=MEAN STDDEV SKEWNESS KURTOSIS.
EXAMINE VARIABLES=Strategic_Mean Tactical_Mean Operational_Mean Decision_Making_Quality
  /PLOT NPPLOT /STATISTICS NONE /NOTOTAL.

* ===== STEP 5: Spearman correlations (non-normal data). ============.
NONPAR CORR VARIABLES=Strategic_Mean Tactical_Mean Operational_Mean Decision_Making_Quality
  /PRINT=SPEARMAN TWOTAIL SIG.

* ===== STEP 6: MAIN regression on factor scores + assumptions. ======.
* Multicollinearity (VIF/TOL), independence (Durbin-Watson), residual.
* normality (histogram, normal P-P), homoscedasticity/linearity (scatter),.
* influence (Cook's, Mahalanobis).
REGRESSION
  /STATISTICS COEFF OUTS CI(95) R ANOVA COLLIN TOL
  /DEPENDENT DMQ1
  /METHOD=ENTER Strategic1 Tactical1 Operational1
  /RESIDUALS DURBIN HISTOGRAM(ZRESID) NORMPROB(ZRESID)
  /SCATTERPLOT=(*ZRESID ,*ZPRED)
  /SAVE COOK MAHAL.

* ===== STEP 7: robustness - composite means. =======================.
REGRESSION
  /STATISTICS COEFF OUTS R ANOVA
  /DEPENDENT Decision_Making_Quality
  /METHOD=ENTER Strategic_Mean Tactical_Mean Operational_Mean.

* ===== STEP 8: BI challenges (Table) + crosstabs. ==================.
DESCRIPTIVES VARIABLES=BI_Training_Limit BI_Cost_Barrier BI_Data_Integration_Issue BI_Flexibility_Issue
  /STATISTICS=MEAN STDDEV.
FREQUENCIES VARIABLES=BI_Training_Limit BI_Cost_Barrier BI_Data_Integration_Issue BI_Flexibility_Issue.
CROSSTABS TABLES=Job_Position BY BI_Training_Limit BI_Cost_Barrier BI_Data_Integration_Issue BI_Flexibility_Issue /CELLS=ROW.
CROSSTABS TABLES=Industry BY BI_Training_Limit BI_Cost_Barrier BI_Data_Integration_Issue BI_Flexibility_Issue /CELLS=ROW.

* ===== STEP 9: sensitivity - drop the most BI-referential DMQ item. ==.
FACTOR VARIABLES=BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /MISSING LISTWISE /PRINT=EXTRACTION /CRITERIA=FACTORS(1) /EXTRACTION=PAF /ROTATION=NOROTATE /SAVE REG(ALL DMQ3).
REGRESSION
  /STATISTICS COEFF OUTS CI(95) R ANOVA
  /DEPENDENT DMQ31
  /METHOD=ENTER Strategic1 Tactical1 Operational1.

* ===== STEP 10: robustness - demographic controls (incl. size). =====.
RECODE Job_Position (1=1)(ELSE=0) INTO Pos_CEO.
RECODE Job_Position (2=1)(ELSE=0) INTO Pos_Senior.
RECODE Job_Position (3=1)(ELSE=0) INTO Pos_Middle.
RECODE Job_Position (4=1)(ELSE=0) INTO Pos_Operational.
RECODE Industry (1=1)(ELSE=0) INTO Ind_Manuf.
RECODE Industry (2=1)(ELSE=0) INTO Ind_Retail.
RECODE Industry (3=1)(ELSE=0) INTO Ind_Service.
RECODE Industry (4=1)(ELSE=0) INTO Ind_Tech.
RECODE Company_Size (2=1)(ELSE=0) INTO Size_50_99.
RECODE Company_Size (3=1)(ELSE=0) INTO Size_99_250.
EXECUTE.
REGRESSION
  /STATISTICS COEFF OUTS R ANOVA COLLIN TOL
  /DEPENDENT DMQ1
  /METHOD=ENTER Strategic1 Tactical1 Operational1
    Pos_CEO Pos_Senior Pos_Middle Pos_Operational
    Ind_Manuf Ind_Retail Ind_Service Ind_Tech
    Size_50_99 Size_99_250.

* ===== STEP 11: scope robustness - firms <=99 employees. ===========.
TEMPORARY.
SELECT IF Company_Size <= 2.
REGRESSION
  /STATISTICS COEFF OUTS R ANOVA
  /DEPENDENT DMQ1
  /METHOD=ENTER Strategic1 Tactical1 Operational1.

* ===== STEP 12: response-style sensitivity. ========================.
* Excludes the 8 retained partial straight-liners (identical answer to.
* all 13 BI/DMQ items but varied on the challenge items).
COMPUTE bi_sd = SD(Strategic_BI_Availability,Strategic_BI_Alternatives,Strategic_BI_Alignment,
  Tactical_BI_Availability,Tactical_BI_Resource_Alloc,Tactical_BI_Data_Decisions,
  Operational_BI_Availability,Operational_BI_Agility,Operational_BI_Quality,
  BI_Improves_Decisions,BI_Speed_Accuracy,BI_Data_Inform,BI_Alternative_Solutions).
EXECUTE.
TEMPORARY.
SELECT IF bi_sd > 0.
REGRESSION
  /STATISTICS COEFF OUTS R ANOVA
  /DEPENDENT DMQ1
  /METHOD=ENTER Strategic1 Tactical1 Operational1.

* ===== STEP 13: group comparisons (optional, non-parametric). =======.
NPAR TESTS /K-W=Strategic_Mean Tactical_Mean Operational_Mean Decision_Making_Quality BY Company_Size(1 3).
NPAR TESTS /K-W=Strategic_Mean Tactical_Mean Operational_Mean Decision_Making_Quality BY Job_Position(1 5).
NPAR TESTS /K-W=Strategic_Mean Tactical_Mean Operational_Mean Decision_Making_Quality BY Industry(1 5).

* ===================================================================.
* NOTE - validity analyses NOT done here (run BI_DMQ_validity.py):.
* convergent (AVE, CR), discriminant (HTMT, Fornell-Larcker), and the.
* four-factor vs one-factor CFA. Base SPSS cannot estimate CFA.
* ===================================================================.
* End of syntax (n=178).
