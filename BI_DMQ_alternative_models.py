# =====================================================================
# BI and Decision-Making Quality in SMEs
# Alternative models and measurement checks for Q1-oriented revision
#
# Purpose:
# 1. Load the cleaned BI_DMQ dataset from SAV or CSV.
# 2. Recreate the original composites.
# 3. Add Overall BI Utilisation and Managerial BI composites.
# 4. Check reliability, alternative CFA models, AVE, CR, Fornell-Larcker,
#    and HTMT.
# 5. Run regression models with dummy-coded demographic controls.
# 6. Run optional sensitivity checks excluding near-straightline cases.
#
# Input expected in the same folder:
#   BI_DMQ_data_coded.sav
# or
#   BI_DMQ_data_coded.csv
#
# Output:
#   BI_DMQ_alternative_models_results.txt
#   BI_DMQ_regression_table.csv
#
# Required packages:
#   python -m pip install pyreadstat pandas numpy scipy semopy statsmodels
# =====================================================================

import os
import warnings
from itertools import combinations

import numpy as np
import pandas as pd
from scipy import stats

try:
    import pyreadstat
except ImportError:
    pyreadstat = None

from semopy import Model, calc_stats
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

warnings.filterwarnings("ignore")

SAV_FILE = "BI_DMQ_data_coded.sav"
CSV_FILE = "BI_DMQ_data_coded.csv"
OUT_TXT = "BI_DMQ_alternative_models_results.txt"
OUT_REG = "BI_DMQ_regression_table.csv"

CONSTRUCTS_ORIGINAL = {
    "Strategic": [
        "Strategic_BI_Availability",
        "Strategic_BI_Alternatives",
        "Strategic_BI_Alignment",
    ],
    "Tactical": [
        "Tactical_BI_Availability",
        "Tactical_BI_Resource_Alloc",
        "Tactical_BI_Data_Decisions",
    ],
    "Operational": [
        "Operational_BI_Availability",
        "Operational_BI_Agility",
        "Operational_BI_Quality",
    ],
    "DMQ": [
        "BI_Improves_Decisions",
        "BI_Speed_Accuracy",
        "BI_Data_Inform",
        "BI_Alternative_Solutions",
    ],
}

BI_ITEMS = (
    CONSTRUCTS_ORIGINAL["Strategic"]
    + CONSTRUCTS_ORIGINAL["Tactical"]
    + CONSTRUCTS_ORIGINAL["Operational"]
)

MANAGERIAL_ITEMS = CONSTRUCTS_ORIGINAL["Strategic"] + CONSTRUCTS_ORIGINAL["Tactical"]
DMQ_ITEMS = CONSTRUCTS_ORIGINAL["DMQ"]
MAIN_ITEMS = BI_ITEMS + DMQ_ITEMS

CHALLENGE_ITEMS = [
    "BI_Training_Limit",
    "BI_Cost_Barrier",
    "BI_Data_Integration_Issue",
    "BI_Flexibility_Issue",
]

ALL_LIKERT_ITEMS = MAIN_ITEMS + CHALLENGE_ITEMS

lines = []


def log(text=""):
    print(text)
    lines.append(str(text))


def load_data():
    if os.path.exists(SAV_FILE):
        if pyreadstat is None:
            raise ImportError("pyreadstat is required to read SAV files.")
        df, meta = pyreadstat.read_sav(SAV_FILE)
        source = SAV_FILE
    elif os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        source = CSV_FILE
    else:
        raise FileNotFoundError(
            f"Neither {SAV_FILE} nor {CSV_FILE} was found in the current folder."
        )

    # Remove fully empty rows if the CSV has them.
    df = df.dropna(how="all").copy()
    return df, source


def check_columns(df):
    required = ["ID", "Company_Size", "Job_Position", "Industry"] + ALL_LIKERT_ITEMS
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError("Missing expected columns: " + ", ".join(missing))


def cronbach_alpha(df, items):
    x = df[items].dropna().astype(float)
    k = x.shape[1]
    if k < 2:
        return np.nan
    item_vars = x.var(axis=0, ddof=1)
    total_var = x.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_vars.sum() / total_var)


def add_composites(df):
    df = df.copy()
    df["Strategic_Mean"] = df[CONSTRUCTS_ORIGINAL["Strategic"]].mean(axis=1)
    df["Tactical_Mean"] = df[CONSTRUCTS_ORIGINAL["Tactical"]].mean(axis=1)
    df["Operational_Mean"] = df[CONSTRUCTS_ORIGINAL["Operational"]].mean(axis=1)
    df["Decision_Making_Quality"] = df[DMQ_ITEMS].mean(axis=1)
    df["Overall_BI_Utilisation"] = df[BI_ITEMS].mean(axis=1)
    df["Managerial_BI"] = df[MANAGERIAL_ITEMS].mean(axis=1)
    return df


def describe_quality(df):
    log("\n--- Data quality checks ---")
    log(f"Rows: {len(df)}")
    log(f"Columns: {len(df.columns)}")
    log(f"Missing values in main Likert items: {int(df[MAIN_ITEMS].isna().sum().sum())}")
    log(f"Missing values in all Likert items: {int(df[ALL_LIKERT_ITEMS].isna().sum().sum())}")
    log(f"Duplicate IDs: {int(df['ID'].duplicated().sum())}")
    log(f"Duplicate full rows: {int(df.duplicated().sum())}")

    out_of_range = {}
    for c in ALL_LIKERT_ITEMS:
        bad = df.loc[~df[c].between(1, 5), "ID"].tolist()
        if bad:
            out_of_range[c] = bad
    log(f"Likert out-of-range columns: {len(out_of_range)}")
    if out_of_range:
        log(out_of_range)

    # Near-straightline flags across all 17 Likert items.
    flags = []
    for _, row in df.iterrows():
        values = row[ALL_LIKERT_ITEMS].dropna().astype(int).tolist()
        if not values:
            continue
        most_common_count = pd.Series(values).value_counts().max()
        if most_common_count >= 16:
            flags.append((int(row["ID"]), int(most_common_count)))
    log(f"Near-straightline cases across 17 items, count >= 16: {flags}")

    # Identical response across 13 main items.
    main_identical = []
    for _, row in df.iterrows():
        values = row[MAIN_ITEMS].dropna().astype(int).tolist()
        if len(set(values)) == 1:
            main_identical.append(int(row["ID"]))
    log(f"All 13 BI and DMQ items identical: {main_identical}")

    # Duplicate item patterns across all 17 Likert items.
    pattern_duplicates = df[df.duplicated(subset=ALL_LIKERT_ITEMS, keep=False)]
    if len(pattern_duplicates) > 0:
        dup_ids = pattern_duplicates["ID"].astype(int).tolist()
    else:
        dup_ids = []
    log(f"Duplicate 17-item response patterns, IDs: {dup_ids}")


def cfa_description(spec):
    return "\n".join(f"{factor} =~ " + " + ".join(items) for factor, items in spec.items())


def fit_cfa(spec, label):
    desc = cfa_description(spec)
    model = Model(desc)
    model.fit(df_global)
    stats_table = calc_stats(model).T

    def get_stat(key):
        try:
            return float(stats_table.loc[key].iloc[0])
        except Exception:
            return np.nan

    fit = {
        "model": label,
        "chi2": get_stat("chi2"),
        "df": get_stat("DoF"),
        "p": get_stat("chi2 p-value"),
        "CFI": get_stat("CFI"),
        "TLI": get_stat("TLI"),
        "RMSEA": get_stat("RMSEA"),
        "AIC": get_stat("AIC"),
        "BIC": get_stat("BIC"),
    }
    return model, fit


def get_standardised_loadings(model):
    inspect = model.inspect(std_est=True)
    loadings = inspect[inspect["op"] == "~"].copy()
    loadings["Est. Std"] = loadings["Est. Std"].astype(float)
    return dict(zip(loadings["lval"], loadings["Est. Std"])), inspect


def ave_cr_for_spec(model, spec):
    lmap, inspect = get_standardised_loadings(model)
    rows = []
    sqrt_ave = {}
    for construct, items in spec.items():
        L = np.array([lmap[i] for i in items], dtype=float)
        ave = float(np.mean(L ** 2))
        cr = float((L.sum() ** 2) / ((L.sum() ** 2) + np.sum(1 - L ** 2)))
        sqrt_ave[construct] = float(np.sqrt(ave))
        rows.append(
            {
                "construct": construct,
                "AVE": ave,
                "CR": cr,
                "sqrtAVE": sqrt_ave[construct],
                "min_loading": float(L.min()),
            }
        )
    return pd.DataFrame(rows), sqrt_ave, inspect


def factor_correlations(inspect, constructs):
    cov = inspect[inspect["op"] == "~~"].copy()
    cov["Est. Std"] = cov["Est. Std"].astype(float)
    names = list(constructs.keys())
    phi = pd.DataFrame(np.eye(len(names)), index=names, columns=names)
    for _, row in cov.iterrows():
        a = row["lval"]
        b = row["rval"]
        if a in names and b in names and a != b:
            phi.loc[a, b] = row["Est. Std"]
            phi.loc[b, a] = row["Est. Std"]
    return phi


def fornell_larcker(phi, sqrt_ave):
    fl = phi.copy()
    for n in fl.index:
        fl.loc[n, n] = sqrt_ave[n]
    breaches = []
    for a, b in combinations(fl.index, 2):
        if abs(phi.loc[a, b]) > min(sqrt_ave[a], sqrt_ave[b]):
            breaches.append(f"{a}-{b}")
    return fl, breaches


def htmt_matrix(df, constructs):
    names = list(constructs.keys())
    out = pd.DataFrame(np.eye(len(names)), index=names, columns=names)
    for a, b in combinations(names, 2):
        inter = df[constructs[a] + constructs[b]].corr().loc[constructs[a], constructs[b]].values
        heterotrait = np.abs(inter).mean()

        ca = df[constructs[a]].corr().values
        cb = df[constructs[b]].corr().values
        monotrait_a = np.abs(ca[np.triu_indices(len(constructs[a]), 1)]).mean()
        monotrait_b = np.abs(cb[np.triu_indices(len(constructs[b]), 1)]).mean()

        value = heterotrait / np.sqrt(monotrait_a * monotrait_b)
        out.loc[a, b] = value
        out.loc[b, a] = value
    return out


def add_dummies(df):
    df = df.copy()

    # Reference categories:
    # Company_Size 1, Job_Position 1, Industry 1
    df["Company_50_99"] = (df["Company_Size"] == 2).astype(int)
    df["Company_99_250"] = (df["Company_Size"] == 3).astype(int)

    df["Job_Senior"] = (df["Job_Position"] == 2).astype(int)
    df["Job_Middle"] = (df["Job_Position"] == 3).astype(int)
    df["Job_Operational"] = (df["Job_Position"] == 4).astype(int)
    df["Job_Other"] = (df["Job_Position"] == 5).astype(int)

    df["Industry_Retail"] = (df["Industry"] == 2).astype(int)
    df["Industry_Service"] = (df["Industry"] == 3).astype(int)
    df["Industry_Technology"] = (df["Industry"] == 4).astype(int)
    df["Industry_Other"] = (df["Industry"] == 5).astype(int)

    return df


CONTROL_VARS = [
    "Company_50_99",
    "Company_99_250",
    "Job_Senior",
    "Job_Middle",
    "Job_Operational",
    "Job_Other",
    "Industry_Retail",
    "Industry_Service",
    "Industry_Technology",
    "Industry_Other",
]


def standardised_betas(df, y, predictors):
    clean = df[[y] + predictors].dropna().copy()
    z = clean.copy()
    for c in [y] + predictors:
        if clean[c].std(ddof=0) > 0:
            z[c] = (clean[c] - clean[c].mean()) / clean[c].std(ddof=0)
    X = sm.add_constant(z[predictors], has_constant="add")
    model = sm.OLS(z[y], X).fit()
    return model.params.drop("const", errors="ignore").to_dict()


def run_ols(df, label, predictors, y="Decision_Making_Quality"):
    clean = df[[y] + predictors].dropna().copy()
    X = sm.add_constant(clean[predictors], has_constant="add")
    model = sm.OLS(clean[y], X).fit()
    robust = model.get_robustcov_results(cov_type="HC3")
    beta = standardised_betas(clean, y, predictors)

    rows = []
    for idx, name in enumerate(model.params.index):
        if name == "const":
            continue
        robust_idx = list(model.params.index).index(name)
        rows.append(
            {
                "model": label,
                "term": name,
                "b": model.params[name],
                "se_HC3": robust.bse[robust_idx],
                "t_HC3": robust.tvalues[robust_idx],
                "p_HC3": robust.pvalues[robust_idx],
                "std_beta": beta.get(name, np.nan),
                "ci95_low": model.conf_int().loc[name, 0],
                "ci95_high": model.conf_int().loc[name, 1],
                "n": int(model.nobs),
                "r2": model.rsquared,
                "adj_r2": model.rsquared_adj,
                "f_pvalue": model.f_pvalue,
            }
        )

    # Influence diagnostics.
    infl = model.get_influence()
    cooks = infl.cooks_distance[0]
    stud_resid = infl.resid_studentized_external
    leverage = infl.hat_matrix_diag

    # VIF.
    vif_rows = []
    X_no_const = clean[predictors].astype(float)
    if X_no_const.shape[1] > 1:
        for i, col in enumerate(X_no_const.columns):
            try:
                vif_rows.append((col, variance_inflation_factor(X_no_const.values, i)))
            except Exception:
                vif_rows.append((col, np.nan))

    summary = {
        "label": label,
        "n": int(model.nobs),
        "r2": model.rsquared,
        "adj_r2": model.rsquared_adj,
        "f_pvalue": model.f_pvalue,
        "max_cooks_d": float(np.max(cooks)),
        "max_abs_studentized_resid": float(np.max(np.abs(stud_resid))),
        "max_leverage": float(np.max(leverage)),
        "max_vif": float(np.nanmax([v for _, v in vif_rows])) if vif_rows else np.nan,
    }

    return pd.DataFrame(rows), summary, pd.DataFrame(vif_rows, columns=["term", "VIF"])


def report_cfa(spec, label):
    model, fit = fit_cfa(spec, label)
    validity, sqrt_ave, inspect = ave_cr_for_spec(model, spec)
    phi = factor_correlations(inspect, spec)
    fl, breaches = fornell_larcker(phi, sqrt_ave)
    htmt = htmt_matrix(df_global, spec)

    log(f"\n--- CFA model: {label} ---")
    log(
        f"Fit: chi2={fit['chi2']:.2f}, df={fit['df']:.0f}, "
        f"CFI={fit['CFI']:.3f}, TLI={fit['TLI']:.3f}, "
        f"RMSEA={fit['RMSEA']:.3f}, AIC={fit['AIC']:.1f}, BIC={fit['BIC']:.1f}"
    )

    log("\nConvergent validity:")
    log(validity.round(3).to_string(index=False))

    log("\nFornell-Larcker matrix:")
    log(fl.round(3).to_string())

    log("Fornell-Larcker breaches: " + (", ".join(breaches) if breaches else "none"))

    log("\nHTMT matrix:")
    log(htmt.round(3).to_string())

    high_htmt = []
    for a, b in combinations(htmt.index, 2):
        if htmt.loc[a, b] > 0.85:
            high_htmt.append(f"{a}-{b}: {htmt.loc[a, b]:.3f}")
    log("HTMT > .85: " + (", ".join(high_htmt) if high_htmt else "none"))

    return fit, validity, fl, htmt


# =====================================================================
# Main run
# =====================================================================

df, source = load_data()
check_columns(df)
df = add_composites(df)
df = add_dummies(df)
df_global = df.copy()

log("=" * 70)
log("BI DMQ alternative model analysis")
log("=" * 70)
log(f"Input file: {source}")
log(f"n = {len(df)}")

describe_quality(df)

log("\n--- Reliability ---")
reliability_sets = {
    "Strategic": CONSTRUCTS_ORIGINAL["Strategic"],
    "Tactical": CONSTRUCTS_ORIGINAL["Tactical"],
    "Operational": CONSTRUCTS_ORIGINAL["Operational"],
    "DMQ": DMQ_ITEMS,
    "Overall_BI_Utilisation": BI_ITEMS,
    "Managerial_BI": MANAGERIAL_ITEMS,
}
for name, items in reliability_sets.items():
    log(f"{name:24s} alpha = {cronbach_alpha(df, items):.3f}  k={len(items)}")

log("\n--- Composite descriptives ---")
desc_cols = [
    "Strategic_Mean",
    "Tactical_Mean",
    "Operational_Mean",
    "Overall_BI_Utilisation",
    "Managerial_BI",
    "Decision_Making_Quality",
]
desc = df[desc_cols].agg(["count", "mean", "std", "min", "max", "skew", "kurt"]).T
log(desc.round(3).to_string())

log("\n--- Spearman correlations ---")
rho = df[desc_cols].corr(method="spearman")
log(rho.round(3).to_string())

# CFA model specifications.
four_factor = CONSTRUCTS_ORIGINAL
one_factor = {"General": MAIN_ITEMS}
two_factor_overall = {
    "OverallBI": BI_ITEMS,
    "DMQ": DMQ_ITEMS,
}
three_factor_managerial = {
    "ManagerialBI": MANAGERIAL_ITEMS,
    "Operational": CONSTRUCTS_ORIGINAL["Operational"],
    "DMQ": DMQ_ITEMS,
}

for spec, label in [
    (four_factor, "Original four-factor model"),
    (one_factor, "One-factor common method comparison"),
    (two_factor_overall, "Two-factor model: Overall BI and DMQ"),
    (three_factor_managerial, "Three-factor model: Managerial BI, Operational BI, and DMQ"),
]:
    try:
        report_cfa(spec, label)
    except Exception as exc:
        log(f"\nCFA failed for {label}: {exc}")

log("\n--- Regression models with dummy-coded controls and HC3 robust SE ---")

models = {
    "M1_controls_only": CONTROL_VARS,
    "M2_three_BI_levels": CONTROL_VARS
    + ["Strategic_Mean", "Tactical_Mean", "Operational_Mean"],
    "M3_overall_BI": CONTROL_VARS + ["Overall_BI_Utilisation"],
    "M4_managerial_operational": CONTROL_VARS + ["Managerial_BI", "Operational_Mean"],
}

all_reg_rows = []
for label, predictors in models.items():
    reg, summ, vif = run_ols(df, label, predictors)
    all_reg_rows.append(reg)

    log(f"\n{label}")
    log(
        f"n={summ['n']}, R2={summ['r2']:.3f}, adj.R2={summ['adj_r2']:.3f}, "
        f"model p={summ['f_pvalue']:.4g}"
    )
    log(
        f"max Cook's D={summ['max_cooks_d']:.3f}, "
        f"max |studentized residual|={summ['max_abs_studentized_resid']:.3f}, "
        f"max leverage={summ['max_leverage']:.3f}, max VIF={summ['max_vif']:.3f}"
    )
    main_terms = [p for p in predictors if p not in CONTROL_VARS]
    if main_terms:
        log(reg[reg["term"].isin(main_terms)].round(4).to_string(index=False))
    else:
        log("Controls-only model.")

reg_table = pd.concat(all_reg_rows, ignore_index=True)
reg_table.to_csv(OUT_REG, index=False)

# Optional sensitivity excluding near-straightline cases.
flag_ids = [43, 101, 107, 142, 166]
df_sens = df[~df["ID"].isin(flag_ids)].copy()

log("\n--- Sensitivity analysis excluding near-straightline IDs 43, 101, 107, 142, 166 ---")
log(f"Sensitivity n = {len(df_sens)}")

for label, predictors in {
    "SENS_M2_three_BI_levels": models["M2_three_BI_levels"],
    "SENS_M3_overall_BI": models["M3_overall_BI"],
    "SENS_M4_managerial_operational": models["M4_managerial_operational"],
}.items():
    reg, summ, vif = run_ols(df_sens, label, predictors)
    log(f"\n{label}")
    log(
        f"n={summ['n']}, R2={summ['r2']:.3f}, adj.R2={summ['adj_r2']:.3f}, "
        f"model p={summ['f_pvalue']:.4g}"
    )
    main_terms = [p for p in predictors if p not in CONTROL_VARS]
    log(reg[reg["term"].isin(main_terms)].round(4).to_string(index=False))

with open(OUT_TXT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

log("\nResults written to:")
log(f"  {OUT_TXT}")
log(f"  {OUT_REG}")
