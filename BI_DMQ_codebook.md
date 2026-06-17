# Codebook

**Study:** Business Intelligence Utilization and Perceived BI-Supported Decision-Making Quality Across Managerial Levels in SMEs in Kent, Southeast England
**Dataset:** `BI_DMQ_data_coded_n178_SPSS_ready_ID_preserved.csv`
**Final N:** 178 respondents
**Instrument:** Online questionnaire (Google Forms), 5-point Likert items
**Ethics:** IRB 2025-006

---

## 1. Provenance and cleaning

| Step | Detail | N |
|---|---|---|
| Raw export | All submitted responses, complete and in range (no missing cells, all item values 1-5) | 188 |
| Consent exclusion | One response selected both consent options ("I Agree, I Do Not Agree"); consent self-contradictory, removed on consent grounds | -1 |
| Careless-responding exclusion | Nine responses gave one identical value to all 17 items, including the reverse-worded challenge items; identical agreement with positively and negatively worded items indicates inattentive responding | -9 |
| **Analysis dataset** | | **178** |

Notes:
- No cases were excluded for missing data or out-of-range values; all 188 were complete and in range. Exclusions are on **consent** and **careless-responding** grounds only.
- **Partial straight-lining retained:** eight respondents gave identical answers across the 13 BI/DMQ items but varied on the challenge items. These were **retained**, since uniform agreement on a coherent positively-worded block can be genuine. They can be removed in a sensitivity check if a reviewer requests it.
- **De-identification:** this dataset contains no submission timestamps, no consent field, no contact details, and no free-text "Other" write-ins (write-ins were coded to category 5 at source). It is safe for public deposit.
- **Company-size wording:** the survey option read "More than 99 Employees" with no stated upper bound; it is treated as the medium-SME band (99-250) consistent with the SME-targeted sampling frame, an assumption stated in the manuscript limitations. One respondent chose a non-standard "Less than 19 Employees" option, folded into band 1 (<50).

---

## 2. Identifier and demographics

| Variable | Label | Type | Values |
|---|---|---|---|
| `ID` | Respondent ID (sequential, post-cleaning) | Numeric | 1-178; arbitrary, non-identifying |
| `Company_Size` | Firm size band | Numeric | 1 = <50; 2 = 50-99; 3 = 99-250 (medium) |
| `Job_Position` | Respondent role | Numeric | 1 = CEO; 2 = Senior Manager; 3 = Middle Manager; 4 = Operational Manager; 5 = Other |
| `Industry` | Industry sector | Numeric | 1 = Manufacturing; 2 = Retail; 3 = Service; 4 = Technology; 5 = Other |

Sample composition (n = 178): Size - <50: 65, 50-99: 62, 99-250: 51. Position - CEO: 13, Senior: 21, Middle: 36, Operational: 30, Other: 78. Industry - Manufacturing: 13, Retail: 46, Service: 52, Technology: 30, Other: 37.

---

## 3. Likert items (all 1 = Strongly Disagree ... 5 = Strongly Agree)

### Strategic BI (construct: Strategic)
| Variable | Source item (abbreviated) |
|---|---|
| `Strategic_BI_Availability` | BI tools are available and regularly used at the strategic level |
| `Strategic_BI_Alternatives` | BI enhances identification of long-term strategic alternatives |
| `Strategic_BI_Alignment` | BI at the strategic level helps align goals with market opportunities |

### Tactical BI (construct: Tactical)
| Variable | Source item (abbreviated) |
|---|---|
| `Tactical_BI_Availability` | BI is used by tactical managers for medium-term analysis |
| `Tactical_BI_Resource_Alloc` | BI improves resource-allocation decisions for tactical managers |
| `Tactical_BI_Data_Decisions` | BI enables tactical managers to identify trends / data-driven decisions |

### Operational BI (construct: Operational)
| Variable | Source item (abbreviated) |
|---|---|
| `Operational_BI_Availability` | Real-time BI improves quick response to daily operations |
| `Operational_BI_Agility` | Operational BI supports agility in timely daily decisions |
| `Operational_BI_Quality` | BI improves accuracy/reliability of short-term decisions |

### Decision-Making Quality (construct: DMQ)
| Variable | Source item (abbreviated) |
|---|---|
| `BI_Improves_Decisions` | BI availability across managerial levels improves decision-making |
| `BI_Speed_Accuracy` | BI increases speed and accuracy of decision-making |
| `BI_Data_Inform` | BI improves informed decisions based on data rather than intuition |
| `BI_Alternative_Solutions` | BI helps identify more alternative solutions to problems |

### BI Challenges (construct: Challenges; analyzed descriptively)
| Variable | Source item (abbreviated) |
|---|---|
| `BI_Cost_Barrier` | Cost of implementing BI is a barrier to effective use |
| `BI_Training_Limit` | Lack of training/technical expertise limits BI use |
| `BI_Flexibility_Issue` | BI systems are not flexible enough to adapt to changing needs |
| `BI_Data_Integration_Issue` | Lack of data integration across departments limits BI |

---

## 4. Constructs and reliability (n = 178)

| Construct | Items | Cronbach's alpha |
|---|---|---|
| Strategic | 3 | .795 |
| Tactical | 3 | .760 |
| Operational | 3 | .773 |
| DMQ | 4 | .843 |
| Challenges | 4 | .635 |

Reliability values above are deterministic and will be reproduced exactly by the SPSS run; the SPSS output remains the document of record.

---

## 5. Derived variables (computed in SPSS, not stored in this file)

| Variable | Definition |
|---|---|
| `Strategic_Mean`, `Tactical_Mean`, `Operational_Mean`, `Decision_Making_Quality` | Mean of the construct's items (descriptives, Spearman correlations, composite-mean robustness model) |
| `Strategic1`, `Tactical1`, `Operational1`, `DMQ1` | Single-factor PAF regression factor scores, one per construct (main regression and demographic-controls model) |
| `DMQ31` | 3-item DMQ factor score with `BI_Improves_Decisions` removed (BI-referential-item sensitivity) |
| `Pos_*`, `Ind_*`, `Size_*` | Dummy variables for the demographic-controls regression (reference categories: Other position, Other industry, <50 size) |

All derived variables are produced by the accompanying SPSS syntax; the SPSS output is the document of record.
