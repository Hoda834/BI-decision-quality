"""
BI-DMQ Analysis v30 - Comprehensive Python Script
Sample: n = 186 (full sample, no exclusions)
Author: Hoda Rezvanjoo

Single-run, reproducible analysis. Covers:
  - Data quality checks
  - Descriptives (item-level and composite-level)
  - Cronbach alpha (per construct + Overall BI + Managerial BI + Challenges)
  - EFA (PAF + Promax) cross-check vs SPSS
  - CFA: four-factor, one-factor, two-factor, three-factor
  - Convergent validity (AVE, CR)
  - Discriminant validity (Fornell-Larcker, HTMT)
  - Harman single-factor test
  - Pearson + Spearman correlations
  - Regression: controls only, three BI levels, Overall BI, Managerial + Operational
    With both standard and HC3 robust SE
  - Sensitivity excluding straight-liners
  - Sensitivity excluding BI-named DMQ items
  - VIF, Durbin-Watson, Cook's D, leverage

Outputs:
  - analysis_output_v30.txt (full text log)
  - tables/*.csv (all tables as CSV for manuscript)
"""

import os
import sys
import json
import warnings
import numpy as np
import pandas as pd
from pathlib import Path

import pyreadstat
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
from factor_analyzer import FactorAnalyzer, calculate_kmo, calculate_bartlett_sphericity
from semopy import Model, calc_stats

warnings.filterwarnings("ignore")

# ============================================================
# 0. CONFIGURATION
# ============================================================

DATA_FILE = "BI_DMQ_data_v30.sav"
OUT_TXT = "analysis_output_v30.txt"
TABLE_DIR = Path("tables_v30")
TABLE_DIR.mkdir(exist_ok=True)

CONSTRUCTS = {
    "Strategic":   ["Strategic_BI_Availability", "Strategic_BI_Alternatives", "Strategic_BI_Alignment"],
    "Tactical":    ["Tactical_BI_Availability", "Tactical_BI_Resource_Alloc", "Tactical_BI_Data_Decisions"],
    "Operational": ["Operational_BI_Availability", "Operational_BI_Agility", "Operational_BI_Quality"],
    "DMQ":         ["BI_Improves_Decisions", "BI_Speed_Accuracy", "BI_Data_Inform", "BI_Alternative_Solutions"],
    "Challenges":  ["BI_Cost_Barrier", "BI_Training_Limit", "BI_Flexibility_Issue", "BI_Data_Integration_Issue"],
}

OVERALL_BI_ITEMS = CONSTRUCTS["Strategic"] + CONSTRUCTS["Tactical"] + CONSTRUCTS["Operational"]
MANAGERIAL_BI_ITEMS = CONSTRUCTS["Strategic"] + CONSTRUCTS["Tactical"]
BI_DMQ_ITEMS = OVERALL_BI_ITEMS + CONSTRUCTS["DMQ"]

# ============================================================
# Helpers
# ============================================================

class Tee:
    """Write to both console and file."""
    def __init__(self, path):
        self.file = open(path, "w", encoding="utf-8")
    def write(self, s):
        sys.__stdout__.write(s)
        self.file.write(s)
    def flush(self):
        sys.__stdout__.flush()
        self.file.flush()
    def close(self):
        self.file.close()

def header(text, char="="):
    line = char * 70
    print(f"\n{line}\n{text}\n{line}")

def sub(text):
    print(f"\n--- {text} ---")

def save_table(df, name):
    p = TABLE_DIR / f"{name}.csv"
    df.to_csv(p, index=True)
    print(f"  [saved: {p}]")

def cronbach_alpha(items_df):
    items_df = items_df.dropna()
    k = items_df.shape[1]
    if k < 2:
        return float("nan")
    item_var = items_df.var(axis=0, ddof=1).sum()
    total_var = items_df.sum(axis=1).var(ddof=1)
    return k / (k - 1) * (1 - item_var / total_var)

def fit_cfa(df, spec, label):
    """Fit a CFA model using semopy and return fit indices + standardized loadings."""
    print(f"\nCFA: {label}")
    try:
        m = Model(spec)
        m.fit(df)
        stats_ = calc_stats(m)
        fit = {
            "chi2":  float(stats_.loc["Value", "chi2"]),
            "df":    float(stats_.loc["Value", "DoF"]),
            "p":     float(stats_.loc["Value", "chi2 p-value"]),
            "CFI":   float(stats_.loc["Value", "CFI"]),
            "TLI":   float(stats_.loc["Value", "TLI"]),
            "RMSEA": float(stats_.loc["Value", "RMSEA"]),
            "SRMR":  float(stats_.loc["Value", "SRMR"]) if "SRMR" in stats_.columns else float("nan"),
            "AIC":   float(stats_.loc["Value", "AIC"]),
            "BIC":   float(stats_.loc["Value", "BIC"]),
        }
        for k, v in fit.items():
            print(f"  {k:6s} = {v:.4f}" if not np.isnan(v) else f"  {k:6s} = NA")
        ins = m.inspect(std_est=True)
        loadings = ins[(ins["op"] == "~") & (ins["lval"].isin(df.columns) == False)].copy()
        loadings = ins[ins["op"] == "~"].copy()
        load_table = loadings[["lval", "rval", "Est. Std"]].rename(
            columns={"lval": "item", "rval": "factor", "Est. Std": "std_loading"}
        )
        return m, fit, load_table
    except Exception as e:
        print(f"  ERROR: {e}")
        return None, None, None

def compute_ave_cr(load_table):
    """Compute AVE and CR per factor from standardized loadings."""
    rows = []
    for factor, sub in load_table.groupby("factor"):
        loadings = sub["std_loading"].astype(float).values
        loadings = loadings[~np.isnan(loadings)]
        if len(loadings) == 0:
            continue
        sum_sq_load = np.sum(loadings ** 2)
        sum_load = np.sum(loadings)
        error_var = np.sum(1 - loadings ** 2)
        ave = sum_sq_load / len(loadings)
        cr = (sum_load ** 2) / (sum_load ** 2 + error_var)
        rows.append({
            "factor": factor,
            "k_items": len(loadings),
            "AVE": ave,
            "CR": cr,
            "sqrt_AVE": np.sqrt(ave),
            "min_loading": loadings.min(),
            "max_loading": loadings.max(),
        })
    return pd.DataFrame(rows).set_index("factor")

def htmt(df, constructs):
    """Heterotrait-Monotrait ratio of correlations."""
    names = list(constructs.keys())
    result = pd.DataFrame(index=names, columns=names, dtype=float)
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            items_a = constructs[a]
            items_b = constructs[b]
            if a == b:
                result.loc[a, b] = 1.0
                continue
            hetero_corrs = []
            for ia in items_a:
                for ib in items_b:
                    hetero_corrs.append(df[[ia, ib]].corr().iloc[0, 1])
            mono_a = []
            for x in range(len(items_a)):
                for y in range(x + 1, len(items_a)):
                    mono_a.append(df[[items_a[x], items_a[y]]].corr().iloc[0, 1])
            mono_b = []
            for x in range(len(items_b)):
                for y in range(x + 1, len(items_b)):
                    mono_b.append(df[[items_b[x], items_b[y]]].corr().iloc[0, 1])
            mono = np.sqrt(np.mean(np.abs(mono_a)) * np.mean(np.abs(mono_b))) if mono_a and mono_b else np.nan
            hetero = np.mean(np.abs(hetero_corrs)) if hetero_corrs else np.nan
            result.loc[a, b] = hetero / mono if mono and not np.isnan(mono) else np.nan
    return result

def fornell_larcker(load_table, factor_corrs):
    """Fornell-Larcker matrix: diagonal = sqrt(AVE), off-diagonal = factor correlations."""
    ave_df = compute_ave_cr(load_table)
    sqrt_ave = ave_df["sqrt_AVE"]
    mat = factor_corrs.copy().astype(float)
    for f in mat.index:
        if f in sqrt_ave.index:
            mat.loc[f, f] = sqrt_ave[f]
    breaches = []
    for a in mat.index:
        for b in mat.columns:
            if a >= b:
                continue
            if abs(mat.loc[a, b]) >= mat.loc[a, a] or abs(mat.loc[a, b]) >= mat.loc[b, b]:
                breaches.append(f"{a}-{b}")
    return mat, breaches

def run_ols(df, y, X_cols, label, hc="HC3"):
    data = df[[y] + X_cols].dropna()
    X = sm.add_constant(data[X_cols])
    model_std = sm.OLS(data[y], X).fit()
    model_rob = sm.OLS(data[y], X).fit(cov_type=hc)
    # Standardised betas
    z = data.copy()
    for c in [y] + X_cols:
        if z[c].std(ddof=1) > 0:
            z[c] = (z[c] - z[c].mean()) / z[c].std(ddof=1)
    Xz = sm.add_constant(z[X_cols])
    model_z = sm.OLS(z[y], Xz).fit()
    # VIF
    vifs = []
    Xv = data[X_cols].copy()
    Xv = sm.add_constant(Xv)
    for i, c in enumerate(Xv.columns):
        if c == "const":
            continue
        try:
            vifs.append((c, variance_inflation_factor(Xv.values, i)))
        except Exception:
            vifs.append((c, np.nan))
    # Influence
    inf = model_std.get_influence()
    cooks = inf.cooks_distance[0]
    lev = inf.hat_matrix_diag
    stud_resid = inf.resid_studentized_internal
    dw = durbin_watson(model_std.resid)
    # Build coefficient table
    rows = []
    for c in X_cols:
        rows.append({
            "term":      c,
            "b":         model_std.params[c],
            "se":        model_std.bse[c],
            "t":         model_std.tvalues[c],
            "p":         model_std.pvalues[c],
            "ci_low":    model_std.conf_int().loc[c, 0],
            "ci_high":   model_std.conf_int().loc[c, 1],
            "se_HC3":    model_rob.bse[c],
            "t_HC3":     model_rob.tvalues[c],
            "p_HC3":     model_rob.pvalues[c],
            "std_beta":  model_z.params[c],
        })
    coef_df = pd.DataFrame(rows)
    print(f"\n{label}")
    print(f"  n = {int(model_std.nobs)}")
    print(f"  R^2 = {model_std.rsquared:.4f}   adj.R^2 = {model_std.rsquared_adj:.4f}")
    print(f"  F = {model_std.fvalue:.3f}   model p = {model_std.f_pvalue:.4g}")
    print(f"  Durbin-Watson = {dw:.3f}")
    print(f"  max VIF = {max([v for _, v in vifs]):.3f}" if vifs else "")
    print(f"  max |stud. resid.| = {np.max(np.abs(stud_resid)):.3f}")
    print(f"  max Cook's D = {np.max(cooks):.4f}")
    print(f"  max leverage = {np.max(lev):.4f}")
    print("\nCoefficients (standard + HC3 robust + standardised):")
    print(coef_df.to_string(index=False))
    print("\nVIF:")
    for c, v in vifs:
        print(f"  {c:30s}  VIF = {v:.3f}")
    return {
        "label": label, "n": int(model_std.nobs),
        "R2": model_std.rsquared, "adjR2": model_std.rsquared_adj,
        "F": model_std.fvalue, "p_F": model_std.f_pvalue,
        "DW": dw, "coefs": coef_df, "vifs": vifs,
    }

# ============================================================
# 1. LOAD AND CHECK
# ============================================================

def main():
    tee = Tee(OUT_TXT)
    sys.stdout = tee
    try:
        header("BI-DMQ ANALYSIS v30  |  n = 186 (full sample)")
        df, meta = pyreadstat.read_sav(DATA_FILE)
        print(f"\nLoaded {DATA_FILE}")
        print(f"  rows = {df.shape[0]}, columns = {df.shape[1]}")

        # 1. Data quality
        header("1. DATA QUALITY CHECKS")
        sub("Missing values in Likert items")
        miss = df[BI_DMQ_ITEMS + CONSTRUCTS["Challenges"]].isna().sum().sum()
        print(f"  Total missing across all 17 Likert items: {miss}")
        sub("Likert range checks (expected 1-5)")
        for c in BI_DMQ_ITEMS + CONSTRUCTS["Challenges"]:
            mn, mx = df[c].min(), df[c].max()
            flag = "" if 1 <= mn and mx <= 5 else "  <- OUT OF RANGE"
            print(f"  {c:35s} min={mn:.0f} max={mx:.0f}{flag}")
        sub("Within-respondent SD across 13 BI/DMQ items")
        df["BI_DMQ_SD"] = df[BI_DMQ_ITEMS].std(axis=1, ddof=1)
        zero_sd = df[df["BI_DMQ_SD"] == 0]
        print(f"  Cases with SD = 0 (perfect straight-line): {len(zero_sd)}")
        if len(zero_sd) > 0:
            print(f"  IDs: {list(zero_sd['ID'].astype(int).values)}")
        sub("Demographic frequencies")
        for d in ["Company_Size", "Job_Position", "Industry"]:
            print(f"\n  {d}:")
            print(df[d].value_counts().sort_index().to_string())

        # 2. Compute composites
        header("2. COMPOSITE VARIABLES")
        for name, items in CONSTRUCTS.items():
            df[f"{name}_Mean"] = df[items].mean(axis=1)
        df["Overall_BI_Mean"] = df[OVERALL_BI_ITEMS].mean(axis=1)
        df["Managerial_BI_Mean"] = df[MANAGERIAL_BI_ITEMS].mean(axis=1)
        print("\nComputed: Strategic_Mean, Tactical_Mean, Operational_Mean, DMQ_Mean,")
        print("          Challenges_Mean, Overall_BI_Mean, Managerial_BI_Mean")

        # 3. Descriptives
        header("3. DESCRIPTIVE STATISTICS")
        sub("Item-level descriptives")
        all_items = BI_DMQ_ITEMS + CONSTRUCTS["Challenges"]
        item_desc = df[all_items].describe().T[["mean", "std", "min", "max"]]
        item_desc["skew"] = df[all_items].skew()
        item_desc["kurtosis"] = df[all_items].kurtosis()
        item_desc = item_desc.round(3)
        print(item_desc.to_string())
        save_table(item_desc, "T1_item_descriptives")
        sub("Composite-level descriptives")
        comps = ["Strategic_Mean", "Tactical_Mean", "Operational_Mean", "DMQ_Mean",
                 "Challenges_Mean", "Overall_BI_Mean", "Managerial_BI_Mean"]
        comp_desc = df[comps].describe().T[["mean", "std", "min", "max"]]
        comp_desc["skew"] = df[comps].skew()
        comp_desc["kurtosis"] = df[comps].kurtosis()
        comp_desc = comp_desc.round(3)
        print(comp_desc.to_string())
        save_table(comp_desc, "T2_composite_descriptives")

        # 4. Reliability
        header("4. RELIABILITY (CRONBACH ALPHA)")
        rel_rows = []
        for name, items in CONSTRUCTS.items():
            a = cronbach_alpha(df[items])
            rel_rows.append({"scale": name, "k": len(items), "alpha": round(a, 3)})
            print(f"  {name:13s} alpha = {a:.3f}  k = {len(items)}")
        for nm, its in [("Overall_BI", OVERALL_BI_ITEMS), ("Managerial_BI", MANAGERIAL_BI_ITEMS)]:
            a = cronbach_alpha(df[its])
            rel_rows.append({"scale": nm, "k": len(its), "alpha": round(a, 3)})
            print(f"  {nm:13s} alpha = {a:.3f}  k = {len(its)}")
        save_table(pd.DataFrame(rel_rows).set_index("scale"), "T3_reliability")

        # 5. KMO & Bartlett
        header("5. KMO & BARTLETT")
        kmo_per, kmo_total = calculate_kmo(df[BI_DMQ_ITEMS])
        chi_sq, p = calculate_bartlett_sphericity(df[BI_DMQ_ITEMS])
        print(f"  KMO (overall)          = {kmo_total:.3f}")
        print(f"  Bartlett's test of sphericity:")
        print(f"     chi2 = {chi_sq:.2f}, p = {p:.4g}")

        # 6. EFA (PAF + Promax)
        header("6. EFA (PAF, PROMAX) ON 13 BI + DMQ ITEMS")
        fa = FactorAnalyzer(n_factors=4, rotation="promax", method="principal")
        fa.fit(df[BI_DMQ_ITEMS])
        ev_all, ev_common = fa.get_eigenvalues()
        loadings = pd.DataFrame(fa.loadings_, index=BI_DMQ_ITEMS,
                                columns=[f"F{i+1}" for i in range(4)]).round(3)
        var_exp = pd.DataFrame(fa.get_factor_variance(),
                               index=["SS_loadings", "Prop_var", "Cum_var"],
                               columns=[f"F{i+1}" for i in range(4)]).round(3)
        print("\nEigenvalues (initial):")
        print(np.round(ev_all, 3))
        print("\nPattern matrix (Promax-rotated loadings):")
        print(loadings.to_string())
        save_table(loadings, "T4_EFA_pattern_matrix")
        print("\nVariance explained:")
        print(var_exp.to_string())
        save_table(var_exp, "T5_EFA_variance")

        # 7. Harman single-factor
        header("7. HARMAN SINGLE-FACTOR TEST (CMV)")
        fa1 = FactorAnalyzer(n_factors=1, rotation=None, method="principal")
        fa1.fit(df[BI_DMQ_ITEMS])
        var1 = fa1.get_factor_variance()
        print(f"  Single factor explains {var1[1][0]*100:.2f}% of variance")
        print(f"  (Threshold for concern: > 50%)")
        if var1[1][0] > 0.5:
            print("  -> ABOVE threshold: report and triangulate with sensitivity analysis")
        else:
            print("  -> Below threshold: CMV unlikely to be a serious concern")

        # 8. CFA models
        header("8. CFA MODELS")
        spec4 = f"""
        Strategic   =~ {' + '.join(CONSTRUCTS["Strategic"])}
        Tactical    =~ {' + '.join(CONSTRUCTS["Tactical"])}
        Operational =~ {' + '.join(CONSTRUCTS["Operational"])}
        DMQ         =~ {' + '.join(CONSTRUCTS["DMQ"])}
        """
        m4, fit4, load4 = fit_cfa(df, spec4, "Four-factor (theoretical model)")
        if m4 is not None:
            save_table(load4, "T6_CFA_4factor_loadings")
            ins4 = m4.inspect(std_est=True)
            corr4 = ins4[(ins4["op"] == "~~") & (ins4["lval"] != ins4["rval"])].copy()
            factor_corr = pd.DataFrame(index=["Strategic", "Tactical", "Operational", "DMQ"],
                                       columns=["Strategic", "Tactical", "Operational", "DMQ"], dtype=float)
            for f in factor_corr.index:
                factor_corr.loc[f, f] = 1.0
            for _, r in corr4.iterrows():
                if r["lval"] in factor_corr.index and r["rval"] in factor_corr.columns:
                    factor_corr.loc[r["lval"], r["rval"]] = r["Est. Std"]
                    factor_corr.loc[r["rval"], r["lval"]] = r["Est. Std"]
            ave_cr = compute_ave_cr(load4)
            print("\nAVE and CR per construct:")
            print(ave_cr.round(3).to_string())
            save_table(ave_cr, "T7_AVE_CR")
            fl_mat, breaches = fornell_larcker(load4, factor_corr)
            print("\nFornell-Larcker matrix (diagonal = sqrt(AVE), off = factor corr):")
            print(fl_mat.round(3).to_string())
            save_table(fl_mat, "T8_Fornell_Larcker")
            if breaches:
                print(f"\nFornell-Larcker breaches: {', '.join(breaches)}")
            else:
                print("\nNo Fornell-Larcker breaches detected.")

        # One-factor for comparison
        spec1 = f"General =~ {' + '.join(BI_DMQ_ITEMS)}"
        m1, fit1, load1 = fit_cfa(df, spec1, "One-factor (CMV comparison)")

        # Two-factor: Overall BI + DMQ
        spec2 = f"""
        OverallBI =~ {' + '.join(OVERALL_BI_ITEMS)}
        DMQ       =~ {' + '.join(CONSTRUCTS["DMQ"])}
        """
        m2, fit2, load2 = fit_cfa(df, spec2, "Two-factor (Overall BI + DMQ)")

        # Three-factor: Managerial + Operational + DMQ
        spec3 = f"""
        ManagerialBI =~ {' + '.join(MANAGERIAL_BI_ITEMS)}
        Operational  =~ {' + '.join(CONSTRUCTS["Operational"])}
        DMQ          =~ {' + '.join(CONSTRUCTS["DMQ"])}
        """
        m3, fit3, load3 = fit_cfa(df, spec3, "Three-factor (Managerial + Operational + DMQ)")

        # CFA fit comparison
        sub("CFA fit comparison")
        fits = []
        for label, fit in [("4-factor", fit4), ("3-factor", fit3),
                           ("2-factor", fit2), ("1-factor", fit1)]:
            if fit is not None:
                fits.append({"model": label, **fit})
        fit_df = pd.DataFrame(fits).set_index("model").round(3)
        print(fit_df.to_string())
        save_table(fit_df, "T9_CFA_fit_comparison")

        # 9. HTMT
        header("9. HTMT (DISCRIMINANT VALIDITY)")
        constructs4 = {k: v for k, v in CONSTRUCTS.items() if k != "Challenges"}
        htmt_mat = htmt(df, constructs4)
        print("\nHTMT matrix:")
        print(htmt_mat.round(3).to_string())
        save_table(htmt_mat, "T10_HTMT")
        print("\nHTMT > 0.85 (strict) flagged:")
        for i in htmt_mat.index:
            for j in htmt_mat.columns:
                if i < j and htmt_mat.loc[i, j] > 0.85:
                    flag = " (also > 0.90 lenient)" if htmt_mat.loc[i, j] > 0.90 else ""
                    print(f"  {i:13s} - {j:13s}  HTMT = {htmt_mat.loc[i, j]:.3f}{flag}")

        # 10. Correlations
        header("10. CORRELATIONS")
        sub("Pearson correlations among composites")
        comp_corr = df[comps].corr(method="pearson").round(3)
        print(comp_corr.to_string())
        save_table(comp_corr, "T11_pearson_correlations")
        sub("Spearman correlations among composites")
        spear_corr = df[comps].corr(method="spearman").round(3)
        print(spear_corr.to_string())
        save_table(spear_corr, "T12_spearman_correlations")
        sub("p-values for Pearson correlations with DMQ_Mean")
        for c in [x for x in comps if x != "DMQ_Mean"]:
            r, p = stats.pearsonr(df[c], df["DMQ_Mean"])
            print(f"  {c:25s} r = {r:.3f}  p = {p:.4g}")

        # 11. Dummy coding for controls
        header("11. CONTROL VARIABLE DUMMY CODING")
        df["CS_50_99"]    = (df["Company_Size"] == 2).astype(int)
        df["CS_100_249"]  = (df["Company_Size"] == 3).astype(int)
        df["JP_SeniorMgr"] = (df["Job_Position"] == 2).astype(int)
        df["JP_MiddleMgr"] = (df["Job_Position"] == 3).astype(int)
        df["JP_OpsMgr"]    = (df["Job_Position"] == 4).astype(int)
        df["JP_Other"]     = (df["Job_Position"] == 5).astype(int)
        df["IND_Retail"]      = (df["Industry"] == 2).astype(int)
        df["IND_Service"]     = (df["Industry"] == 3).astype(int)
        df["IND_Technology"]  = (df["Industry"] == 4).astype(int)
        df["IND_Other"]       = (df["Industry"] == 5).astype(int)
        CONTROLS = ["CS_50_99", "CS_100_249",
                    "JP_SeniorMgr", "JP_MiddleMgr", "JP_OpsMgr", "JP_Other",
                    "IND_Retail", "IND_Service", "IND_Technology", "IND_Other"]
        print("Reference categories: Company_Size = <50, Job_Position = CEO, Industry = Manufacturing")

        # 12. Regression models
        header("12. REGRESSION MODELS (n = 186)")
        results = {}
        results["M1"] = run_ols(df, "DMQ_Mean", CONTROLS, "M1: Controls only")
        results["M2"] = run_ols(df, "DMQ_Mean", ["Strategic_Mean", "Tactical_Mean", "Operational_Mean"],
                                "M2: Three BI levels (PRIMARY, no controls)")
        results["M3"] = run_ols(df, "DMQ_Mean", CONTROLS + ["Strategic_Mean", "Tactical_Mean", "Operational_Mean"],
                                "M3: Three BI levels + controls (robustness)")
        results["M4"] = run_ols(df, "DMQ_Mean", CONTROLS + ["Overall_BI_Mean"],
                                "M4: Overall BI + controls (robustness)")
        results["M5"] = run_ols(df, "DMQ_Mean", CONTROLS + ["Managerial_BI_Mean", "Operational_Mean"],
                                "M5: Managerial + Operational + controls (robustness)")

        # Save consolidated regression table
        all_coefs = []
        for k, r in results.items():
            tmp = r["coefs"].copy()
            tmp.insert(0, "model", k)
            tmp.insert(1, "n", r["n"])
            tmp.insert(2, "R2", r["R2"])
            tmp.insert(3, "adjR2", r["adjR2"])
            all_coefs.append(tmp)
        all_reg = pd.concat(all_coefs, ignore_index=True)
        save_table(all_reg, "T13_regression_all_models")

        # 13. Sensitivity: exclude straight-liners
        header("13. SENSITIVITY: EXCLUDE STRAIGHT-LINERS")
        df_sens = df[df["BI_DMQ_SD"] > 0].copy()
        print(f"\nn after excluding straight-liners = {len(df_sens)}")
        run_ols(df_sens, "DMQ_Mean",
                CONTROLS + ["Strategic_Mean", "Tactical_Mean", "Operational_Mean"],
                "M3_sensitivity: Three BI levels + controls (excluding straight-liners)")

        # 14. Sensitivity: drop most BI-anchored DMQ item
        header("14. SENSITIVITY: BI-ANCHORED DMQ ITEM REMOVED")
        # Following the approach described in the manuscript: remove the most
        # directly BI-anchored DMQ item (BI_Improves_Decisions), which most
        # explicitly names BI as the source of improved decisions, and recompute
        # the DMQ composite from the remaining three items.
        df["DMQ_3item"] = df[["BI_Speed_Accuracy", "BI_Data_Inform", "BI_Alternative_Solutions"]].mean(axis=1)
        run_ols(df, "DMQ_3item",
                ["Strategic_Mean", "Tactical_Mean", "Operational_Mean"],
                "M_DMQ_3item: BI_Improves_Decisions removed, DMQ from 3 items")
        run_ols(df, "DMQ_3item",
                CONTROLS + ["Strategic_Mean", "Tactical_Mean", "Operational_Mean"],
                "M_DMQ_3item_controls: BI_Improves_Decisions removed + controls")

        # 15. Save processed dataset for repo
        header("15. SAVE PROCESSED DATASET")
        out_csv = "BI_DMQ_data_v30_processed.csv"
        df.to_csv(out_csv, index=False)
        print(f"  Saved: {out_csv}")

        # Summary
        header("16. SUMMARY TABLE OF KEY RESULTS")
        summary = pd.DataFrame({
            "metric": [
                "n",
                "Cronbach alpha Strategic", "Cronbach alpha Tactical",
                "Cronbach alpha Operational", "Cronbach alpha DMQ",
                "KMO", "Harman 1-factor % variance",
                "CFA 4-factor CFI", "CFA 4-factor TLI", "CFA 4-factor RMSEA",
                "CFA 4-factor chi2/df",
                "Primary model R^2 (M2, no controls)",
                "Primary model adj. R^2",
                "Controlled robustness R^2 (M3, with controls)",
                "Controlled robustness adj. R^2",
                "Sensitivity (no straight-liners) R^2",
            ],
            "value": [
                len(df),
                round(cronbach_alpha(df[CONSTRUCTS["Strategic"]]), 3),
                round(cronbach_alpha(df[CONSTRUCTS["Tactical"]]), 3),
                round(cronbach_alpha(df[CONSTRUCTS["Operational"]]), 3),
                round(cronbach_alpha(df[CONSTRUCTS["DMQ"]]), 3),
                round(kmo_total, 3),
                round(var1[1][0]*100, 2),
                round(fit4["CFI"], 3) if fit4 else "NA",
                round(fit4["TLI"], 3) if fit4 else "NA",
                round(fit4["RMSEA"], 3) if fit4 else "NA",
                round(fit4["chi2"]/fit4["df"], 3) if fit4 else "NA",
                round(results["M2"]["R2"], 3),
                round(results["M2"]["adjR2"], 3),
                round(results["M3"]["R2"], 3),
                round(results["M3"]["adjR2"], 3),
                "see section 13",
            ],
        })
        print(summary.to_string(index=False))
        save_table(summary, "T14_summary")

        header("ANALYSIS COMPLETE")
        print(f"\nFull log: {OUT_TXT}")
        print(f"Tables directory: {TABLE_DIR}/")
    finally:
        sys.stdout = sys.__stdout__
        tee.close()

if __name__ == "__main__":
    main()
