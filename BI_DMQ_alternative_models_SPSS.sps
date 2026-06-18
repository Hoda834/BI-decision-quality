* =====================================================================.
* BI and Decision-Making Quality in SMEs
* Alternative model syntax for Q1-oriented robustness reporting.
*
* Purpose:
* 1. Keep the original three-level BI model.
* 2. Add an Overall BI Utilisation model.
* 3. Add a Managerial BI plus Operational BI model.
* 4. Use dummy-coded demographic controls rather than treating categories
*    as continuous variables.
* 5. Add optional sensitivity analysis excluding near-straightline cases.
*
* Before running:
* - Either open BI_DMQ_data_coded.sav in SPSS first, or edit the GET FILE
*   path below and remove the leading asterisk.
* - The expected item names match the cleaned n = 178 dataset.
* =====================================================================.

* Optional direct file load. Edit path if needed.
* GET FILE='C:\Users\hrezv\Downloads\1\BI_DMQ_data_coded.sav'.

DATASET NAME BI_DMQ_178 WINDOW=FRONT.

* =====================================================================.
* STEP 1. Construct composite variables.
* =====================================================================.

COMPUTE Strategic_Mean = MEAN(Strategic_BI_Availability,
                              Strategic_BI_Alternatives,
                              Strategic_BI_Alignment).

COMPUTE Tactical_Mean = MEAN(Tactical_BI_Availability,
                             Tactical_BI_Resource_Alloc,
                             Tactical_BI_Data_Decisions).

COMPUTE Operational_Mean = MEAN(Operational_BI_Availability,
                                Operational_BI_Agility,
                                Operational_BI_Quality).

COMPUTE Decision_Making_Quality = MEAN(BI_Improves_Decisions,
                                       BI_Speed_Accuracy,
                                       BI_Data_Inform,
                                       BI_Alternative_Solutions).

COMPUTE Overall_BI_Utilisation = MEAN(Strategic_BI_Availability,
                                      Strategic_BI_Alternatives,
                                      Strategic_BI_Alignment,
                                      Tactical_BI_Availability,
                                      Tactical_BI_Resource_Alloc,
                                      Tactical_BI_Data_Decisions,
                                      Operational_BI_Availability,
                                      Operational_BI_Agility,
                                      Operational_BI_Quality).

COMPUTE Managerial_BI = MEAN(Strategic_BI_Availability,
                             Strategic_BI_Alternatives,
                             Strategic_BI_Alignment,
                             Tactical_BI_Availability,
                             Tactical_BI_Resource_Alloc,
                             Tactical_BI_Data_Decisions).
EXECUTE.

VARIABLE LABELS
 Strategic_Mean "Strategic BI mean score"
 Tactical_Mean "Tactical BI mean score"
 Operational_Mean "Operational BI mean score"
 Decision_Making_Quality "BI-supported decision-making quality mean score"
 Overall_BI_Utilisation "Overall BI utilisation mean score across strategic, tactical, and operational items"
 Managerial_BI "Managerial BI mean score across strategic and tactical items".

FORMATS Strategic_Mean Tactical_Mean Operational_Mean Decision_Making_Quality
        Overall_BI_Utilisation Managerial_BI (F8.3).

* =====================================================================.
* STEP 2. Reliability checks for alternative composites.
* =====================================================================.

RELIABILITY
 /VARIABLES=Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
 /SCALE('Strategic BI') ALL
 /MODEL=ALPHA
 /SUMMARY=TOTAL.

RELIABILITY
 /VARIABLES=Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
 /SCALE('Tactical BI') ALL
 /MODEL=ALPHA
 /SUMMARY=TOTAL.

RELIABILITY
 /VARIABLES=Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
 /SCALE('Operational BI') ALL
 /MODEL=ALPHA
 /SUMMARY=TOTAL.

RELIABILITY
 /VARIABLES=BI_Improves_Decisions BI_Speed_Accuracy BI_Data_Inform BI_Alternative_Solutions
 /SCALE('Decision-Making Quality') ALL
 /MODEL=ALPHA
 /SUMMARY=TOTAL.

RELIABILITY
 /VARIABLES=Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
            Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
            Operational_BI_Availability Operational_BI_Agility Operational_BI_Quality
 /SCALE('Overall BI Utilisation') ALL
 /MODEL=ALPHA
 /SUMMARY=TOTAL.

RELIABILITY
 /VARIABLES=Strategic_BI_Availability Strategic_BI_Alternatives Strategic_BI_Alignment
            Tactical_BI_Availability Tactical_BI_Resource_Alloc Tactical_BI_Data_Decisions
 /SCALE('Managerial BI') ALL
 /MODEL=ALPHA
 /SUMMARY=TOTAL.

* =====================================================================.
* STEP 3. Descriptives and non-parametric correlations.
* =====================================================================.

DESCRIPTIVES VARIABLES=Strategic_Mean Tactical_Mean Operational_Mean
                       Overall_BI_Utilisation Managerial_BI Decision_Making_Quality
 /STATISTICS=MEAN STDDEV MIN MAX SKEWNESS KURTOSIS.

NONPAR CORR
 /VARIABLES=Strategic_Mean Tactical_Mean Operational_Mean
            Overall_BI_Utilisation Managerial_BI Decision_Making_Quality
 /PRINT=SPEARMAN TWOTAIL
 /MISSING=PAIRWISE.

* =====================================================================.
* STEP 4. Dummy-code categorical controls.
* Reference groups:
* Company_Size: 1 = <50 employees
* Job_Position: 1 = CEO
* Industry: 1 = Manufacturing
* =====================================================================.

NUMERIC Company_50_99 Company_99_250
        Job_Senior Job_Middle Job_Operational Job_Other
        Industry_Retail Industry_Service Industry_Technology Industry_Other (F1.0).

COMPUTE Company_50_99 = (Company_Size = 2).
COMPUTE Company_99_250 = (Company_Size = 3).

COMPUTE Job_Senior = (Job_Position = 2).
COMPUTE Job_Middle = (Job_Position = 3).
COMPUTE Job_Operational = (Job_Position = 4).
COMPUTE Job_Other = (Job_Position = 5).

COMPUTE Industry_Retail = (Industry = 2).
COMPUTE Industry_Service = (Industry = 3).
COMPUTE Industry_Technology = (Industry = 4).
COMPUTE Industry_Other = (Industry = 5).
EXECUTE.

VARIABLE LABELS
 Company_50_99 "Company size 50 to 99 employees, reference <50"
 Company_99_250 "Company size 99 to 250 employees, reference <50"
 Job_Senior "Senior manager, reference CEO"
 Job_Middle "Middle manager, reference CEO"
 Job_Operational "Operational manager, reference CEO"
 Job_Other "Other job position, reference CEO"
 Industry_Retail "Retail industry, reference Manufacturing"
 Industry_Service "Service industry, reference Manufacturing"
 Industry_Technology "Technology industry, reference Manufacturing"
 Industry_Other "Other industry, reference Manufacturing".

VALUE LABELS Company_50_99 Company_99_250
             Job_Senior Job_Middle Job_Operational Job_Other
             Industry_Retail Industry_Service Industry_Technology Industry_Other
 0 "No" 1 "Yes".

* =====================================================================.
* STEP 5. Regression models for reporting.
*
* Model 1: controls only.
* Model 2: original three-level BI model.
* Model 3: overall BI utilisation model.
* Model 4: managerial BI plus operational BI model.
*
* Output needed for manuscript:
* - R square and adjusted R square
* - R square change from controls
* - standardised beta, p value, 95% CI
* - VIF and Tolerance
* - Durbin-Watson
* - residual plots and influence diagnostics
* =====================================================================.

REGRESSION
 /DEPENDENT Decision_Making_Quality
 /METHOD=ENTER Company_50_99 Company_99_250
               Job_Senior Job_Middle Job_Operational Job_Other
               Industry_Retail Industry_Service Industry_Technology Industry_Other
 /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN CI(95)
 /RESIDUALS HISTOGRAM(ZRESID) NORMPROB(ZRESID)
 /SCATTERPLOT=(*ZPRED,*ZRESID)
 /SAVE ZPRED ZRESID COOK MAHAL.

REGRESSION
 /DEPENDENT Decision_Making_Quality
 /METHOD=ENTER Company_50_99 Company_99_250
               Job_Senior Job_Middle Job_Operational Job_Other
               Industry_Retail Industry_Service Industry_Technology Industry_Other
 /METHOD=ENTER Strategic_Mean Tactical_Mean Operational_Mean
 /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN CI(95)
 /RESIDUALS HISTOGRAM(ZRESID) NORMPROB(ZRESID)
 /SCATTERPLOT=(*ZPRED,*ZRESID)
 /SAVE ZPRED ZRESID COOK MAHAL.

REGRESSION
 /DEPENDENT Decision_Making_Quality
 /METHOD=ENTER Company_50_99 Company_99_250
               Job_Senior Job_Middle Job_Operational Job_Other
               Industry_Retail Industry_Service Industry_Technology Industry_Other
 /METHOD=ENTER Overall_BI_Utilisation
 /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN CI(95)
 /RESIDUALS HISTOGRAM(ZRESID) NORMPROB(ZRESID)
 /SCATTERPLOT=(*ZPRED,*ZRESID)
 /SAVE ZPRED ZRESID COOK MAHAL.

REGRESSION
 /DEPENDENT Decision_Making_Quality
 /METHOD=ENTER Company_50_99 Company_99_250
               Job_Senior Job_Middle Job_Operational Job_Other
               Industry_Retail Industry_Service Industry_Technology Industry_Other
 /METHOD=ENTER Managerial_BI Operational_Mean
 /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN CI(95)
 /RESIDUALS HISTOGRAM(ZRESID) NORMPROB(ZRESID)
 /SCATTERPLOT=(*ZPRED,*ZRESID)
 /SAVE ZPRED ZRESID COOK MAHAL.

* Influence summary for saved diagnostic variables.
* SPSS will create names such as ZPR_1, ZRE_1, COO_1, MAH_1, then ZPR_2, etc.
DISPLAY DICTIONARY.

* =====================================================================.
* STEP 6. Optional sensitivity analysis.
*
* These are the five near-straightline cases previously flagged for
* sensitivity testing only: ID 43, 101, 107, 142, 166.
* Do not use this as the main analysis unless you explicitly justify it.
* =====================================================================.

USE ALL.
NUMERIC Sensitivity_Keep (F1.0).
COMPUTE Sensitivity_Keep = (ID <> 43 AND ID <> 101 AND ID <> 107 AND ID <> 142 AND ID <> 166).
FILTER BY Sensitivity_Keep.
EXECUTE.

FREQUENCIES VARIABLES=Sensitivity_Keep.

REGRESSION
 /DEPENDENT Decision_Making_Quality
 /METHOD=ENTER Company_50_99 Company_99_250
               Job_Senior Job_Middle Job_Operational Job_Other
               Industry_Retail Industry_Service Industry_Technology Industry_Other
 /METHOD=ENTER Strategic_Mean Tactical_Mean Operational_Mean
 /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN CI(95).

REGRESSION
 /DEPENDENT Decision_Making_Quality
 /METHOD=ENTER Company_50_99 Company_99_250
               Job_Senior Job_Middle Job_Operational Job_Other
               Industry_Retail Industry_Service Industry_Technology Industry_Other
 /METHOD=ENTER Overall_BI_Utilisation
 /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN CI(95).

REGRESSION
 /DEPENDENT Decision_Making_Quality
 /METHOD=ENTER Company_50_99 Company_99_250
               Job_Senior Job_Middle Job_Operational Job_Other
               Industry_Retail Industry_Service Industry_Technology Industry_Other
 /METHOD=ENTER Managerial_BI Operational_Mean
 /STATISTICS COEFF OUTS R ANOVA CHANGE COLLIN CI(95).

FILTER OFF.
USE ALL.
EXECUTE.

* =====================================================================.
* END.
* =====================================================================.
