# Business Intelligence as a Differentiated Decision-Support Capability: A Multi-Level Analysis of SMEs' Decision-Making Quality

Data and analysis files supporting the manuscript "Business Intelligence as a Differentiated Decision-Support Capability: A Multi-Level Analysis of SMEs' Decision-Making Quality". The study examines business intelligence utilisation and perceived decision-making quality in small and medium-sized enterprises in Kent, United Kingdom.

**Author:** Hoda Rezvanjoo, DBA
**ORCID:** <https://orcid.org/0009-0006-3882-2669>
**IRB approval:** 2025-006

## Contents

| File | Description |
|---|---|
| data_anonymised.csv | Raw item-level survey responses (n = 186), anonymised |
| data_processed.csv | Same cases with SPSS-generated factor scores, z-scores, composite means, and diagnostics |
| codebook.md | Variable definitions, coding, and scale information |
| SPSS_syntax_verification.sps | Full SPSS analysis syntax |
| SPSS_output.pdf | SPSS output of record |
| survey_instrument.pdf | Questionnaire as administered |

## Study summary

A cross-sectional survey of 186 managers in small and medium-sized enterprises in Kent, United Kingdom, examining how business intelligence utilisation at the strategic, tactical, and operational levels relates to perceived decision-making quality. Analyses include per-construct Principal Axis Factoring, a combined Harman single-factor test, Spearman correlations, multiple regression on saved factor scores with diagnostics, and a robustness regression on composite means.

## Anonymisation

Submission timestamps were removed prior to deposit. No names, contact details, IP addresses, or firm identifiers were collected in the deposited variables.

## Reproducing the analysis

1. Open `SPSS_syntax_verification.sps` in IBM SPSS Statistics.
2. Load `data_anonymised.csv` as the active dataset. The `GET DATA` command at the top of the syntax points to a local file path, so update that path to wherever you have saved `data_anonymised.csv`.
3. Run the syntax in full. It produces the frequencies, descriptives, correlations, factor analyses (including the Harman single-factor test), and both regression models reported in the manuscript.

`data_processed.csv` contains the derived variables this syntax generates, included for verification without rerunning.

## License

Data and documentation are released under [CC-BY-4.0](LICENSE.md). Please cite the manuscript when reusing.
