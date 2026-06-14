* ===================================================================.
* BI and Decision-Making Quality in SMEs - Analysis Syntax.
* Dataset: DataSet1.csv (n = 186).
* Run each block in order. Output is the document of record.
* ===================================================================.

* Variable coding:
*   Job_Position  1=CEO  2=Senior Manager  3=Middle Manager
*                 4=Operational Manager  5=Other.
*   Industry      1=Manufacturing  2=Retail  3=Services
*                 4=Technology  5=Other.
*   All BI and DMQ items: 5-point Likert (1=Strongly Disagree ... 5=Strongly Agree).

* ===================================================================.
* STEP 0: Demographics (Table 1).
* ===================================================================.
FREQUENCIES VARIABLES=Job_Position Industry.

* ===================================================================.
* STEP 1: Reliability (Table 2 alphas).
* ===================================================================.
RELIABILITY VARIABLES=Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
  /SCALE('Strategic BI') ALL /MODEL=ALPHA.
RELIABILITY VARIABLES=Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
  /SCALE('Tactical BI') ALL /MODEL=ALPHA.
RELIABILITY VARIABLES=Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
  /SCALE('Operational BI') ALL /MODEL=ALPHA.
RELIABILITY VARIABLES=BI_Improves_Decisions BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /SCALE('DMQ') ALL /MODEL=ALPHA.
RELIABILITY VARIABLES=BI_Training_Limit BI_Cost_Barrier BI_Data_Integration_Issue BI_Flexibility_Issue
  /SCALE('Challenges') ALL /MODEL=ALPHA.

* ===================================================================.
* STEP 2: Per-construct EFA (Table 2 loadings, KMO, Bartlett, %variance).
* Principal Axis Factoring, single factor. Read FACTOR MATRIX for loadings.
* Read EXTRACTION SUMS OF SQUARED LOADINGS for % variance.
* ===================================================================.
FACTOR VARIABLES=Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
  /PRINT=KMO EXTRACTION /CRITERIA=FACTORS(1) /EXTRACTION=PAF /ROTATION=NOROTATE.
FACTOR VARIABLES=Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
  /PRINT=KMO EXTRACTION /CRITERIA=FACTORS(1) /EXTRACTION=PAF /ROTATION=NOROTATE.
FACTOR VARIABLES=Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
  /PRINT=KMO EXTRACTION /CRITERIA=FACTORS(1) /EXTRACTION=PAF /ROTATION=NOROTATE.
FACTOR VARIABLES=BI_Improves_Decisions BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /PRINT=KMO EXTRACTION /CRITERIA=FACTORS(1) /EXTRACTION=PAF /ROTATION=NOROTATE.

* ===================================================================.
* STEP 3: Harman single-factor test (Section 3.4).
* All 13 items, one unrotated factor.
* Report FIRST FACTOR % from the SAME column you cite in 3.4 and 5.4.
* (Initial Eigenvalues column ~54%; Extraction Sums column ~51%.)
* ===================================================================.
FACTOR VARIABLES=Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
  Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
  Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
  BI_Improves_Decisions BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /PRINT=EXTRACTION /CRITERIA=FACTORS(1) /EXTRACTION=PAF /ROTATION=NOROTATE.

* ===================================================================.
* STEP 4: Descriptives + normality (Table 3 M/SD, skew, kurtosis).
* ===================================================================.
DESCRIPTIVES VARIABLES=Strategic_Mean Tactical_Mean Operational_Mean Decision_Making_Quality
  /STATISTICS=MEAN STDDEV SKEWNESS KURTOSIS.

* ===================================================================.
* STEP 5: Spearman correlations (Table 3) on composite means.
* ===================================================================.
NONPAR CORR VARIABLES=Strategic_Mean Tactical_Mean Operational_Mean Decision_Making_Quality
  /PRINT=SPEARMAN TWOTAIL SIG.

* ===================================================================.
* STEP 6: Main regression on FACTOR SCORES (Table 4, R2, F, betas, CIs,
* VIF/tolerance, Durbin-Watson, Cook's, Mahalanobis).
* Cases must be in original file order for Durbin-Watson.
* ===================================================================.
REGRESSION
  /STATISTICS COEFF OUTS CI(95) R ANOVA COLLIN TOL
  /DEPENDENT DMQ_Factor
  /METHOD=ENTER Strategic_Factor Tactical_Factor Operational_Factor
  /RESIDUALS DURBIN
  /SAVE COOK MAHAL.

* ===================================================================.
* STEP 7: Robustness check on standardized composite means (Section 4.3).
* ===================================================================.
REGRESSION
  /STATISTICS COEFF OUTS R ANOVA
  /DEPENDENT Decision_Making_Quality
  /METHOD=ENTER Strategic_Mean Tactical_Mean Operational_Mean.

* ===================================================================.
* STEP 8: BI challenges (Table 5) M/SD and agreement %.
* Agreement % = proportion answering 4 or 5; read from frequency tables.
* ===================================================================.
DESCRIPTIVES VARIABLES=BI_Training_Limit BI_Cost_Barrier BI_Data_Integration_Issue BI_Flexibility_Issue
  /STATISTICS=MEAN STDDEV.
FREQUENCIES VARIABLES=BI_Training_Limit BI_Cost_Barrier BI_Data_Integration_Issue BI_Flexibility_Issue.

* Cross-tabs by position and industry (Sections 4.4 and 5.3).
CROSSTABS TABLES=Job_Position BY BI_Training_Limit BI_Cost_Barrier BI_Data_Integration_Issue BI_Flexibility_Issue
  /CELLS=ROW.
CROSSTABS TABLES=Industry BY BI_Training_Limit BI_Cost_Barrier BI_Data_Integration_Issue BI_Flexibility_Issue
  /CELLS=ROW.

* End of syntax.

* ===================================================================.
* STEP 9: Sensitivity analysis - DMQ with the most BI-referential item.
* removed (Section 4.4, Robustness Check).
* Drops BI_Improves_Decisions (item references strategic/tactical/operational
* BI explicitly), re-derives a 3-item DMQ factor score, and re-runs the model.
* ===================================================================.
FACTOR
  /VARIABLES BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /MISSING LISTWISE
  /ANALYSIS BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /EXTRACTION PAF
  /CRITERIA FACTORS(1)
  /ROTATION NOROTATE
  /SAVE REG(ALL DMQ3).
* SPSS names the saved score DMQ31 (rootname + factor number, no underscore).
* Sign is arbitrary; loadings are positive here so betas come out positive.
* If DMQ31 already exists from a prior run, SPSS will create DMQ32 instead;
* in that case run the FACTOR block on a freshly loaded dataset.

REGRESSION
  /STATISTICS COEFF OUTS CI(95) R ANOVA
  /DEPENDENT DMQ31
  /METHOD=ENTER Strategic_Factor Tactical_Factor Operational_Factor.

* Expected (Section 4.4): R2 = .559; Operational beta = .347 (p<.001),.
* Tactical = .252 (p=.002), Strategic = .236 (p=.003).

* ===================================================================.
* NOTE on CFA and HTMT (Section 4.2, Discriminant Validity).
* Base SPSS Statistics does not estimate confirmatory factor models. The
* four-factor vs one-factor CFA reported in the manuscript was estimated by
* maximum likelihood in a CFA-capable tool (e.g., AMOS, JASP, or R lavaan).
* HTMT is computed from the inter-item correlation matrix. Both are reproduced
* in the accompanying script cfa_htmt_sensitivity.py.
* ===================================================================.

* End of syntax (v2).
