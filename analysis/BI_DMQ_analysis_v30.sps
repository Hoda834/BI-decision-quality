* =====================================================================
* BI-DMQ Analysis v30 - Comprehensive SPSS Syntax
* Sample: n = 186 (full sample, no exclusions)
* Author: Hoda Rezvanjoo
* Purpose: Single-run, reproducible analysis for journal submission
* =====================================================================

* -------------------- 0. SETUP --------------------
* Adjust GET FILE path to where you saved the .sav file.

GET FILE='BI_DMQ_data_v30.sav'.
DATASET NAME RawData WINDOW=FRONT.

* Variable labels for demographics.
VARIABLE LABELS
  Company_Size 'Company size band (1=<50, 2=50-99, 3=100-249)'
  Job_Position 'Job position (1=CEO, 2=Senior Manager, 3=Middle Manager, 4=Operational Manager, 5=Other)'
  Industry 'Industry (1=Manufacturing, 2=Retail, 3=Service, 4=Technology, 5=Other)'.

VALUE LABELS Company_Size 1 '<50 employees' 2 '50-99 employees' 3 '100-249 employees'.
VALUE LABELS Job_Position 1 'CEO' 2 'Senior Manager' 3 'Middle Manager' 4 'Operational Manager' 5 'Other'.
VALUE LABELS Industry 1 'Manufacturing' 2 'Retail' 3 'Service' 4 'Technology' 5 'Other'.

EXECUTE.

* -------------------- 1. DATA QUALITY CHECKS --------------------

* 1a. Sample size and missing values.
DESCRIPTIVES VARIABLES=ALL /STATISTICS=MEAN STDDEV MIN MAX.

* 1b. Frequency of demographics.
FREQUENCIES VARIABLES=Company_Size Job_Position Industry
  /STATISTICS=NONE.

* 1c. Identify near-straightline cases (zero variance across 13 BI/DMQ items).
COMPUTE BI_DMQ_SD = SD(Strategic_BI_Availability, Strategic_BI_Alternatives, Strategic_BI_Alignment,
                      Tactical_BI_Availability, Tactical_BI_Resource_Alloc, Tactical_BI_Data_Decisions,
                      Operational_BI_Availability, Operational_BI_Agility, Operational_BI_Quality,
                      BI_Improves_Decisions, BI_Speed_Accuracy, BI_Data_Inform, BI_Alternative_Solutions).
VARIABLE LABELS BI_DMQ_SD 'Within-respondent SD across 13 BI/DMQ items'.
EXECUTE.

FREQUENCIES VARIABLES=BI_DMQ_SD /STATISTICS=NONE /FORMAT=NOTABLE
  /HISTOGRAM.

* List IDs with SD = 0 (perfect straight-liners).
TEMPORARY.
SELECT IF (BI_DMQ_SD = 0).
LIST VARIABLES=ID Company_Size Job_Position Industry.

* -------------------- 2. COMPUTE COMPOSITE MEANS --------------------

COMPUTE Strategic_Mean = MEAN(Strategic_BI_Availability, Strategic_BI_Alternatives, Strategic_BI_Alignment).
COMPUTE Tactical_Mean = MEAN(Tactical_BI_Availability, Tactical_BI_Resource_Alloc, Tactical_BI_Data_Decisions).
COMPUTE Operational_Mean = MEAN(Operational_BI_Availability, Operational_BI_Agility, Operational_BI_Quality).
COMPUTE DMQ_Mean = MEAN(BI_Improves_Decisions, BI_Speed_Accuracy, BI_Data_Inform, BI_Alternative_Solutions).
COMPUTE Challenges_Mean = MEAN(BI_Cost_Barrier, BI_Training_Limit, BI_Flexibility_Issue, BI_Data_Integration_Issue).
COMPUTE Overall_BI_Mean = MEAN(Strategic_BI_Availability, Strategic_BI_Alternatives, Strategic_BI_Alignment,
                                Tactical_BI_Availability, Tactical_BI_Resource_Alloc, Tactical_BI_Data_Decisions,
                                Operational_BI_Availability, Operational_BI_Agility, Operational_BI_Quality).
COMPUTE Managerial_BI_Mean = MEAN(Strategic_BI_Availability, Strategic_BI_Alternatives, Strategic_BI_Alignment,
                                   Tactical_BI_Availability, Tactical_BI_Resource_Alloc, Tactical_BI_Data_Decisions).
EXECUTE.

VARIABLE LABELS
  Strategic_Mean 'Strategic BI utilisation composite'
  Tactical_Mean 'Tactical BI utilisation composite'
  Operational_Mean 'Operational BI utilisation composite'
  DMQ_Mean 'Decision-making quality composite'
  Challenges_Mean 'BI challenges composite'
  Overall_BI_Mean 'Overall BI utilisation (all 9 items)'
  Managerial_BI_Mean 'Managerial BI (Strategic + Tactical)'.

* -------------------- 3. DESCRIPTIVES OF COMPOSITES --------------------

DESCRIPTIVES VARIABLES=Strategic_Mean Tactical_Mean Operational_Mean DMQ_Mean
                      Challenges_Mean Overall_BI_Mean Managerial_BI_Mean
  /STATISTICS=MEAN STDDEV MIN MAX SKEWNESS KURTOSIS.

* Item-level descriptives.
DESCRIPTIVES VARIABLES=Strategic_BI_Availability TO BI_Data_Integration_Issue
  /STATISTICS=MEAN STDDEV MIN MAX SKEWNESS KURTOSIS.

* -------------------- 4. RELIABILITY (CRONBACH ALPHA) --------------------

RELIABILITY
  /VARIABLES=Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
  /SCALE('Strategic BI') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE
  /SUMMARY=TOTAL.

RELIABILITY
  /VARIABLES=Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
  /SCALE('Tactical BI') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE
  /SUMMARY=TOTAL.

RELIABILITY
  /VARIABLES=Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
  /SCALE('Operational BI') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE
  /SUMMARY=TOTAL.

RELIABILITY
  /VARIABLES=BI_Improves_Decisions BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /SCALE('DMQ') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE
  /SUMMARY=TOTAL.

RELIABILITY
  /VARIABLES=BI_Cost_Barrier BI_Training_Limit BI_Flexibility_Issue BI_Data_Integration_Issue
  /SCALE('Challenges') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE
  /SUMMARY=TOTAL.

RELIABILITY
  /VARIABLES=Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
             Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
             Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
  /SCALE('Overall BI') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE
  /SUMMARY=TOTAL.

RELIABILITY
  /VARIABLES=Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
             Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
  /SCALE('Managerial BI') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE
  /SUMMARY=TOTAL.

* -------------------- 5. EFA (PAF, PROMAX) ON 13 BI + DMQ ITEMS --------------------

* 5a. KMO and Bartlett.
* 5b. Principal Axis Factoring with Promax rotation.
* 5c. Primary regression uses standardized composite mean scores (Section 9), not factor scores.

FACTOR
  /VARIABLES Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
             Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
             Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
             BI_Improves_Decisions BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /MISSING LISTWISE
  /ANALYSIS Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
             Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
             Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
             BI_Improves_Decisions BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /PRINT INITIAL KMO REPR EXTRACTION ROTATION
  /FORMAT SORT BLANK(.30)
  /CRITERIA FACTORS(4) ITERATE(25)
  /EXTRACTION PAF
  /CRITERIA ITERATE(25)
  /ROTATION PROMAX(4)
  /METHOD=CORRELATION.

* Note: Factor scores are not saved. Primary regression uses standardized
* composite mean scores (see Section 9).

* -------------------- 6. HARMAN SINGLE-FACTOR TEST (CMV) --------------------

FACTOR
  /VARIABLES Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
             Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
             Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
             BI_Improves_Decisions BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /MISSING LISTWISE
  /ANALYSIS Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
             Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
             Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
             BI_Improves_Decisions BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
  /PRINT INITIAL EXTRACTION
  /CRITERIA FACTORS(1) ITERATE(25)
  /EXTRACTION PAF
  /ROTATION NOROTATE
  /METHOD=CORRELATION.

* -------------------- 7. CORRELATIONS --------------------

* 7a. Pearson correlations among composites.
CORRELATIONS
  /VARIABLES=Strategic_Mean Tactical_Mean Operational_Mean DMQ_Mean
             Overall_BI_Mean Managerial_BI_Mean Challenges_Mean
  /PRINT=TWOTAIL NOSIG FULL
  /MISSING=PAIRWISE.

* 7b. Spearman correlations (robustness for ordinal data).
NONPAR CORR
  /VARIABLES=Strategic_Mean Tactical_Mean Operational_Mean DMQ_Mean
             Overall_BI_Mean Managerial_BI_Mean Challenges_Mean
  /PRINT=SPEARMAN TWOTAIL NOSIG FULL
  /MISSING=PAIRWISE.

* -------------------- 8. CONTROL VARIABLE DUMMY CODING --------------------

* Company_Size: reference = 1 (<50 employees).
RECODE Company_Size (2=1)(ELSE=0) INTO CS_50_99.
RECODE Company_Size (3=1)(ELSE=0) INTO CS_100_249.

* Job_Position: reference = 1 (CEO).
RECODE Job_Position (2=1)(ELSE=0) INTO JP_SeniorMgr.
RECODE Job_Position (3=1)(ELSE=0) INTO JP_MiddleMgr.
RECODE Job_Position (4=1)(ELSE=0) INTO JP_OpsMgr.
RECODE Job_Position (5=1)(ELSE=0) INTO JP_Other.

* Industry: reference = 1 (Manufacturing).
RECODE Industry (2=1)(ELSE=0) INTO IND_Retail.
RECODE Industry (3=1)(ELSE=0) INTO IND_Service.
RECODE Industry (4=1)(ELSE=0) INTO IND_Technology.
RECODE Industry (5=1)(ELSE=0) INTO IND_Other.

EXECUTE.

VARIABLE LABELS
  CS_50_99 'Company size 50-99 (ref: <50)'
  CS_100_249 'Company size 100-249 (ref: <50)'
  JP_SeniorMgr 'Job: Senior Manager (ref: CEO)'
  JP_MiddleMgr 'Job: Middle Manager (ref: CEO)'
  JP_OpsMgr 'Job: Operational Manager (ref: CEO)'
  JP_Other 'Job: Other (ref: CEO)'
  IND_Retail 'Industry: Retail (ref: Manufacturing)'
  IND_Service 'Industry: Service (ref: Manufacturing)'
  IND_Technology 'Industry: Technology (ref: Manufacturing)'
  IND_Other 'Industry: Other (ref: Manufacturing)'.

* -------------------- 9. MAIN REGRESSION (Composite means -> DMQ) --------------------

* Model M1: Controls only.
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN TOL CI(95)
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT DMQ_Mean
  /METHOD=ENTER CS_50_99 CS_100_249 JP_SeniorMgr JP_MiddleMgr JP_OpsMgr JP_Other
                IND_Retail IND_Service IND_Technology IND_Other
  /RESIDUALS DURBIN HISTOGRAM(ZRESID) NORMPROB(ZRESID)
  /CASEWISE PLOT(ZRESID) OUTLIERS(3)
  /SAVE COOK LEVER ZRESID.

* Model M2: Three BI levels -> DMQ (PRIMARY MODEL, no controls).
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN TOL CI(95) ZPP
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT DMQ_Mean
  /METHOD=ENTER Strategic_Mean Tactical_Mean Operational_Mean
  /RESIDUALS DURBIN HISTOGRAM(ZRESID) NORMPROB(ZRESID)
  /CASEWISE PLOT(ZRESID) OUTLIERS(3)
  /SCATTERPLOT=(*ZRESID ,*ZPRED).

* Model M3: Three BI levels + controls -> DMQ (controlled robustness check).
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN TOL CI(95) ZPP
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT DMQ_Mean
  /METHOD=ENTER CS_50_99 CS_100_249 JP_SeniorMgr JP_MiddleMgr JP_OpsMgr JP_Other
                IND_Retail IND_Service IND_Technology IND_Other
  /METHOD=ENTER Strategic_Mean Tactical_Mean Operational_Mean
  /RESIDUALS DURBIN HISTOGRAM(ZRESID) NORMPROB(ZRESID)
  /CASEWISE PLOT(ZRESID) OUTLIERS(3)
  /SCATTERPLOT=(*ZRESID ,*ZPRED).

* -------------------- 10. ROBUSTNESS: ALTERNATIVE SPECIFICATIONS --------------------

* M4: Overall BI (single composite) -> DMQ.
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN TOL CI(95)
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT DMQ_Mean
  /METHOD=ENTER CS_50_99 CS_100_249 JP_SeniorMgr JP_MiddleMgr JP_OpsMgr JP_Other
                IND_Retail IND_Service IND_Technology IND_Other Overall_BI_Mean
  /RESIDUALS DURBIN.

* M5: Managerial BI + Operational BI -> DMQ.
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN TOL CI(95)
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT DMQ_Mean
  /METHOD=ENTER CS_50_99 CS_100_249 JP_SeniorMgr JP_MiddleMgr JP_OpsMgr JP_Other
                IND_Retail IND_Service IND_Technology IND_Other
                Managerial_BI_Mean Operational_Mean
  /RESIDUALS DURBIN.

* -------------------- 11. SENSITIVITY: EXCLUDING STRAIGHT-LINERS --------------------

* Re-run primary model excluding cases with SD = 0 across 13 BI/DMQ items.
TEMPORARY.
SELECT IF (BI_DMQ_SD > 0).
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN TOL CI(95)
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT DMQ_Mean
  /METHOD=ENTER CS_50_99 CS_100_249 JP_SeniorMgr JP_MiddleMgr JP_OpsMgr JP_Other
                IND_Retail IND_Service IND_Technology IND_Other
  /METHOD=ENTER Strategic_Mean Tactical_Mean Operational_Mean.

* -------------------- 12. SENSITIVITY: BI-NAMED DMQ ITEM REMOVED --------------------

* Following v29's described approach: remove the most directly BI-anchored DMQ item
* (BI_Improves_Decisions, which most explicitly states that BI improves decisions)
* and recompute the DMQ composite from the remaining three items.
* This bounds the definitional component of the BI-DMQ association.

COMPUTE DMQ_3item = MEAN(BI_Speed_Accuracy, BI_Data_Inform, BI_Alternative_Solutions).
EXECUTE.
VARIABLE LABELS DMQ_3item 'DMQ composite (3 items, BI_Improves_Decisions removed)'.

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN TOL CI(95)
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT DMQ_3item
  /METHOD=ENTER Strategic_Mean Tactical_Mean Operational_Mean
  /RESIDUALS DURBIN.

* -------------------- 13. SAVE PROCESSED FILE --------------------

SAVE OUTFILE='BI_DMQ_data_v30_processed.sav'
  /COMPRESSED.

* -------------------- END OF SYNTAX --------------------
