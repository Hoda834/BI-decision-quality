"""
cfa_htmt_sensitivity.py
-----------------------
Reproduces the discriminant-validity and sensitivity analyses reported in
Section 4.2 (Discriminant Validity) and Section 4.4 (Robustness Check) of the
manuscript. Base SPSS Statistics does not estimate confirmatory factor models,
so these analyses are provided as a reproducible supplement to the SPSS syntax.

Inputs : DataSet1.csv (item-level responses; same file used by the SPSS syntax)
Outputs: prints the four-factor vs one-factor CFA comparison, the HTMT matrix,
         and the item-removed sensitivity regression.

Requirements:
    pip install pandas numpy scipy statsmodels factor_analyzer semopy

Run:
    python cfa_htmt_sensitivity.py
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from scipy.stats import chi2
import statsmodels.api as sm
from factor_analyzer import FactorAnalyzer
from semopy import Model, calc_stats

DATA = "DataSet1.csv"

ITEMS = {
    "STR": ["Strategic_BI_Availability", "Strategic_BI_Alternatives", "Strategic_BI_Alignment"],
    "TAC": ["Tactical_BI_Availability", "Tactical_BI_Resource_Alloc", "Tactical_BI_Data_Decisions"],
    "OPR": ["Operational_BI_Availability", "Operational_BI_Agility", "Operational_BI_Quality"],
    "DMQ": ["BI_Improves_Decisions", "BI_Speed_Accuracy", "BI_Data_Inform", "BI_Alternative_Solutions"],
}
ALL_ITEMS = [i for v in ITEMS.values() for i in v]


def z(s):
    return (s - s.mean()) / s.std(ddof=1)


def run_cfa(data):
    """Four-factor (hypothesized) vs one-factor (common method) CFA, ML estimation."""
    m4_desc = "\n".join(f"{k} =~ " + " + ".join(v) for k, v in ITEMS.items())
    m1_desc = "G =~ " + " + ".join(ALL_ITEMS)

    def fit(desc, label):
        m = Model(desc)
        m.fit(data)
        st = calc_stats(m).T
        g = lambda k: float(st.loc[k].iloc[0])
        chi, dof = g("chi2"), g("DoF")
        print(f"{label:30s} chi2={chi:7.2f}  df={dof:.0f}  chi2/df={chi/dof:.2f}  "
              f"CFI={g('CFI'):.3f}  TLI={g('TLI'):.3f}  RMSEA={g('RMSEA'):.3f}")
        return chi, dof

    print("\n=== Confirmatory Factor Analysis (Section 4.2) ===")
    c4, d4 = fit(m4_desc, "Four-factor (hypothesized)")
    c1, d1 = fit(m1_desc, "One-factor (common method)")
    dchi, ddf = c1 - c4, int(d1 - d4)
    p = chi2.sf(dchi, ddf)
    print(f"Chi-square difference: d_chi2={dchi:.2f}, d_df={ddf}, p={p:.3e}  "
          f"-> {'four-factor fits better' if p < 0.05 else 'no difference'}")


def htmt(R, a, b):
    inter = [R.loc[x, y] for x in ITEMS[a] for y in ITEMS[b]]
    def mono(c):
        it = ITEMS[c]
        v = [R.loc[it[i], it[j]] for i in range(len(it)) for j in range(i + 1, len(it))]
        return np.mean(v)
    return np.mean(inter) / np.sqrt(mono(a) * mono(b))


def run_htmt(df):
    print("\n=== HTMT ratios (Section 4.2; concern > 0.85, serious > 0.90) ===")
    R = df[ALL_ITEMS].corr()
    keys = list(ITEMS)
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            print(f"  {keys[i]:4s}-{keys[j]:4s}: {htmt(R, keys[i], keys[j]):.3f}")


def run_sensitivity(df):
    """Drop the most BI-referential DMQ item and re-run the regression."""
    print("\n=== Sensitivity: DMQ item 'BI_Improves_Decisions' removed (Section 4.4) ===")
    X = df[["Strategic_Factor", "Tactical_Factor", "Operational_Factor"]].copy()
    X.columns = ["Strategic", "Tactical", "Operational"]
    dmq3 = ["BI_Speed_Accuracy", "BI_Data_Inform", "BI_Alternative_Solutions"]
    fa = FactorAnalyzer(n_factors=1, rotation=None, method="principal")
    fa.fit(df[dmq3])
    y = z(pd.Series(fa.transform(df[dmq3])[:, 0], index=df.index))
    # align sign so loadings are positive (sign is arbitrary in factor extraction)
    if np.corrcoef(y, df[dmq3].mean(axis=1))[0, 1] < 0:
        y = -y
    m = sm.OLS(y, sm.add_constant(X)).fit()
    print(f"  R2={m.rsquared:.3f}  adjR2={m.rsquared_adj:.3f}  F={m.fvalue:.2f}")
    for n in ["Strategic", "Tactical", "Operational"]:
        print(f"  {n:11s} beta={m.params[n]:+.3f}  t={m.tvalues[n]:.2f}  p={m.pvalues[n]:.4f}")


def main():
    df = pd.read_csv(DATA)
    print(f"Loaded {DATA}: n = {len(df)}")
    run_cfa(df[ALL_ITEMS].copy())
    run_htmt(df)
    run_sensitivity(df)


if __name__ == "__main__":
    main()
