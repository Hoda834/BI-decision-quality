# BI–Decision-Making Quality in Kent SMEs

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0006--3882--2669-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0006-3882-2669)

This repository contains the de-identified dataset, full analysis syntax (SPSS and Python), reproducible outputs, and the survey instrument supporting the study:

> **Business Intelligence Utilization and Perceived BI-Supported Decision-Making Quality across Strategic, Tactical, and Operational Managerial Levels in Kent SMEs**

A pre-print is deposited on SSRN: **DOI: 10.2139/ssrn.6465540**

---

## Repository structure

```
BI-decision-quality/
├── README.md                          This file
├── LICENSE                            CC-BY-4.0
├── codebook.md                        Variable definitions, value labels, item wording
│
├── data/
│   ├── BI_DMQ_data_v30.sav            SPSS native format, n=186
│   └── BI_DMQ_data_v30.csv            CSV equivalent
│
├── analysis/
│   ├── BI_DMQ_analysis_v30.sps        SPSS syntax (reproduces all in-text statistics)
│   ├── BI_DMQ_analysis_v30.py         Python script (adds CFA, AVE/CR, HTMT)
│   ├── SPSS_output_v30.pdf            Full SPSS output as PDF
│   ├── analysis_output_v30.txt        Full Python text log
│   └── tables/                        14 separate CSV tables (descriptives, reliability,
│                                      EFA, CFA fit, AVE/CR, Fornell-Larcker, HTMT,
│                                      correlations, regression coefficients, summary)
│
└── survey/
    └── survey_instrument.pdf          Questionnaire as administered
```

---

## How to reproduce the analyses

### SPSS
1. Open `analysis/BI_DMQ_analysis_v30.sps`
2. Verify the `GET FILE` path points to `data/BI_DMQ_data_v30.sav`
3. **Run All**
4. Export output to PDF for archiving

### Python
```
pip install pyreadstat factor_analyzer semopy statsmodels pandas numpy scipy
python analysis/BI_DMQ_analysis_v30.py
```
This regenerates `analysis_output_v30.txt` and the `tables/` folder. The Python script additionally computes CFA fit indices, AVE/CR, Fornell-Larcker, and HTMT, which SPSS does not produce natively.

---

## Key results

| Metric | Value |
|---|---|
| Sample size | 186 |
| Cronbach α (Strategic, Tactical, Operational, DMQ) | 0.800, 0.768, 0.781, 0.845 |
| KMO | 0.936 |
| CFA four-factor: CFI / TLI / RMSEA | 0.965 / 0.954 / 0.065 |
| Primary regression R² (composite means, no controls) | 0.630 |
| Strategic β | 0.264, p < 0.001 |
| Tactical β | 0.263, p = 0.001 |
| Operational β | 0.359, p < 0.001 |
| Controlled robustness R² (with company size, industry, job position) | 0.648 |
| Sensitivity (no straight-liners, n = 171) R² | 0.621 |
| Sensitivity (most BI-anchored DMQ item removed) R² | 0.557 |
| Harman single-factor variance | 54.42% |

Discriminant validity is limited: several HTMT values exceed 0.85 (highest: Strategic–Tactical = 0.959). The strategic and tactical dimensions are theoretically distinct but empirically intertwined in this SME sample. See the manuscript for full discussion.

---

## License

Data, syntax, and outputs are released under the [Creative Commons Attribution 4.0 International License (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/). You are free to share and adapt the material with appropriate attribution.

---

## Citation

If you use any material from this repository, please cite the associated manuscript and this repository.

> Rezvanjoo, H. (forthcoming). BI utilization and perceived BI-supported decision-making quality across managerial levels in Kent SMEs.

After publication, this README will be updated with the journal DOI.

---

## Contact

For questions about the data or analysis:
[ORCID: 0009-0006-3882-2669](https://orcid.org/0009-0006-3882-2669)
