# Codebook: BI-DMQ Dataset (v30)

**Study:** Business Intelligence Utilization and Perceived BI-Supported Decision-Making Quality across Strategic, Tactical, and Operational Managerial Levels in Kent SMEs

**Author:** Hoda Rezvanjoo
**ORCID:** 0009-0006-3882-2669
**IRB:** 2025-006
**Sample:** n = 186 SME managers, Kent (Southeast England)
**Collection:** Cross-sectional online survey, Google Forms
**License:** CC-BY-4.0

---

## File contents

- `BI_DMQ_data_v30.sav` — SPSS native format
- `BI_DMQ_data_v30.csv` — CSV with same content, UTF-8 encoded

Both files contain 186 rows and 21 columns. No missing values in any Likert item.

---

## Variable list

| # | Variable | Type | Range | Description |
|---|---|---|---|---|
| 1 | `ID` | int | 1–186 | Respondent identifier |
| 2 | `Company_Size` | categorical (1–3) | — | Company size band |
| 3 | `Job_Position` | categorical (1–5) | — | Respondent's job position |
| 4 | `Industry` | categorical (1–5) | — | Industry sector |
| 5 | `Strategic_BI_Availability` | Likert 1–5 | 1–5 | Strategic BI item 1 |
| 6 | `Strategic_BI_Alternatives` | Likert 1–5 | 1–5 | Strategic BI item 2 |
| 7 | `Strategic_BI_Alignment` | Likert 1–5 | 1–5 | Strategic BI item 3 |
| 8 | `Tactical_BI_Availability` | Likert 1–5 | 1–5 | Tactical BI item 1 |
| 9 | `Tactical_BI_Resource_Alloc` | Likert 1–5 | 1–5 | Tactical BI item 2 |
| 10 | `Tactical_BI_Data_Decisions` | Likert 1–5 | 1–5 | Tactical BI item 3 |
| 11 | `Operational_BI_Availability` | Likert 1–5 | 1–5 | Operational BI item 1 |
| 12 | `Operational_BI_Agility` | Likert 1–5 | 1–5 | Operational BI item 2 |
| 13 | `Operational_BI_Quality` | Likert 1–5 | 1–5 | Operational BI item 3 |
| 14 | `BI_Improves_Decisions` | Likert 1–5 | 1–5 | DMQ item 1 |
| 15 | `BI_Speed_Accuracy` | Likert 1–5 | 1–5 | DMQ item 2 |
| 16 | `BI_Data_Inform` | Likert 1–5 | 1–5 | DMQ item 3 |
| 17 | `BI_Alternative_Solutions` | Likert 1–5 | 1–5 | DMQ item 4 |
| 18 | `BI_Cost_Barrier` | Likert 1–5 | 1–5 | Challenge item 1 |
| 19 | `BI_Training_Limit` | Likert 1–5 | 1–5 | Challenge item 2 |
| 20 | `BI_Flexibility_Issue` | Likert 1–5 | 1–5 | Challenge item 3 |
| 21 | `BI_Data_Integration_Issue` | Likert 1–5 | 1–5 | Challenge item 4 |

---

## Likert scale

All Likert items use the same 5-point scale:

| Code | Label |
|---|---|
| 1 | Strongly Disagree |
| 2 | Disagree |
| 3 | Neutral |
| 4 | Agree |
| 5 | Strongly Agree |

---

## Demographic value labels

### Company_Size
| Code | Label | Frequency | % |
|---|---|---|---|
| 1 | Under 50 employees | 63 | 33.9 |
| 2 | 50–99 employees | 72 | 38.7 |
| 3 | 100–249 employees | 51 | 27.4 |

*Note:* One respondent selected a non-standard "Less than 19 Employees" option (an artifact of the form), which was folded into band 1 (<50 employees). Company size was captured in three broad categorical bands rather than as independently verified employee counts.

### Job_Position
| Code | Label | Frequency | % |
|---|---|---|---|
| 1 | CEO | 13 | 7.0 |
| 2 | Senior Manager | 22 | 11.8 |
| 3 | Middle Manager | 37 | 19.9 |
| 4 | Operational Manager | 36 | 19.4 |
| 5 | Other | 78 | 41.9 |

*Note:* Free-text descriptions of "Other" job positions were stripped during anonymization and are not available.

### Industry
| Code | Label | Frequency | % |
|---|---|---|---|
| 1 | Manufacturing | 14 | 7.5 |
| 2 | Retail | 51 | 27.4 |
| 3 | Service | 53 | 28.5 |
| 4 | Technology | 31 | 16.7 |
| 5 | Other | 37 | 19.9 |

---

## Item wording (from survey instrument)

### Strategic BI (Section 2)
- `Strategic_BI_Availability`: "BI tools are available and regularly used at the strategic level of management in your organisation."
- `Strategic_BI_Alternatives`: "BI enhances the identification of long-term strategic alternatives in your organisation."
- `Strategic_BI_Alignment`: "The availability of BI at the strategic level helps align business goals with market opportunities."

### Tactical BI (Section 3)
- `Tactical_BI_Availability`: "BI tools are actively used by tactical managers to analyse and support medium-term operational goals."
- `Tactical_BI_Resource_Alloc`: "BI tools improve resource allocation decisions by providing tactical managers with accurate and timely data."
- `Tactical_BI_Data_Decisions`: "BI enhances data-driven decisions by enabling tactical managers to identify trends and align actions with organisational goals."

### Operational BI (Section 4)
- `Operational_BI_Availability`: "Real-time BI tools enhance managers' ability to respond quickly and effectively to daily operational challenges."
- `Operational_BI_Agility`: "Operational BI supports agility by enabling managers to make informed and timely daily decisions."
- `Operational_BI_Quality`: "BI tools enhance the accuracy and reliability of short-term decisions by providing detailed operational data."

### Decision-Making Quality (Section 5)
- `BI_Improves_Decisions`: "The availability of BI at different managerial levels (strategic, tactical, operational) improves the overall decision-making process."
- `BI_Speed_Accuracy`: "BI increases the speed and accuracy of decision-making in your organisation."
- `BI_Data_Inform`: "BI tools have improved the ability to make informed decisions based on data rather than intuition or guesswork."
- `BI_Alternative_Solutions`: "BI has led to the identification of more alternative solutions to problems within the organisation."

### BI Challenges (Section 6)
- `BI_Cost_Barrier`: "The cost of implementing BI tools is a barrier to effective utilisation in your organisation."
- `BI_Training_Limit`: "Lack of training and technical expertise limits the full use of BI in decision-making processes."
- `BI_Flexibility_Issue`: "BI systems in place are not flexible enough to adapt to changing business needs."
- `BI_Data_Integration_Issue`: "There is a lack of data integration across different departments, limiting the effectiveness of BI."

---

## Derived variables (computed during analysis, not in raw file)

These variables are computed by the SPSS syntax and Python script:

| Variable | Formula |
|---|---|
| `Strategic_Mean` | mean of 3 Strategic BI items |
| `Tactical_Mean` | mean of 3 Tactical BI items |
| `Operational_Mean` | mean of 3 Operational BI items |
| `DMQ_Mean` | mean of 4 DMQ items |
| `Challenges_Mean` | mean of 4 Challenge items |
| `Overall_BI_Mean` | mean of all 9 BI items |
| `Managerial_BI_Mean` | mean of Strategic + Tactical items (6 items) |
| `DMQ_3item` | sensitivity composite: DMQ minus BI_Improves_Decisions |
| Dummy variables | `CS_50_99`, `CS_100_249`, `JP_*`, `IND_*` for regression controls |

---

## Data quality notes

- **Missing values:** Zero. All 186 respondents completed all 17 Likert items.
- **Likert range:** All items fall within the expected 1–5 range.
- **Sample size:** 186 valid responses retained for all analyses. Two responses were removed during initial screening for failing predefined validity checks.
- **Within-respondent variance:** 15 respondents (8.1%) showed zero variance across the 13 BI and DMQ items. These cases were retained in the primary analysis, with a sensitivity check excluding them (n = 171) reported in the manuscript.
- **Response rate:** Because recruitment used indirect distribution through shared workspace communities and onward sharing, the number of individuals who received the invitation could not be verified; a formal response rate cannot be computed.

---

## How to use

### SPSS
1. Open `BI_DMQ_data_v30.sav`
2. Open `BI_DMQ_analysis_v30.sps`
3. Run All
4. Output reproduces tables and statistics reported in the manuscript

### Python
```
pip install pyreadstat factor_analyzer semopy statsmodels pandas numpy scipy
python BI_DMQ_analysis_v30.py
```
Produces `analysis_output_v30.txt` and CSV tables in `tables_v30/`. Python output includes CFA fit indices, AVE/CR, HTMT matrix, and Fornell-Larcker matrix that SPSS does not compute natively.

---

## Citation

If you use this dataset, please cite the associated manuscript and this repository:

> Rezvanjoo, H. (forthcoming). BI utilization and perceived BI-supported decision-making quality across managerial levels in Kent SMEs.

A pre-print version of this study is available on SSRN:
DOI: 10.2139/ssrn.6465540
