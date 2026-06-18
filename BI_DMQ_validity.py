"""
BI-DMQ study: validity analyses that base SPSS cannot perform.
Covers protocol items 18-20, 22 (AVE/CR, HTMT, Fornell-Larcker, CFA 4F vs 1F,
full-collinearity VIF). Run after the SPSS pipeline. Output here is a
supplementary record; cite alongside the SPSS output.

Requires: pandas, numpy, semopy   (pip install semopy)
"""
import pandas as pd, numpy as np, semopy, warnings
warnings.filterwarnings('ignore')

DATA = "BI_DMQ_data_coded_n178_SPSS_ready_ID_preserved.csv"
df = pd.read_csv(DATA)

CONSTRUCTS = {
 'Strategic':   ['Strategic_BI_Availability','Strategic_BI_Alternatives','Strategic_BI_Alignment'],
 'Tactical':    ['Tactical_BI_Availability','Tactical_BI_Resource_Alloc','Tactical_BI_Data_Decisions'],
 'Operational': ['Operational_BI_Availability','Operational_BI_Agility','Operational_BI_Quality'],
 'DMQ':         ['BI_Improves_Decisions','BI_Speed_Accuracy','BI_Data_Inform','BI_Alternative_Solutions'],
}
all_items = [i for v in CONSTRUCTS.values() for i in v]

def fit_cfa(spec):
    m = semopy.Model(spec); m.fit(df)
    s = semopy.calc_stats(m).loc['Value']
    return m, s

def srmr(model):
    obs = np.corrcoef(df[all_items].values, rowvar=False)
    Sig = model.calc_sigma()[0]
    d = np.sqrt(np.diag(Sig)); imp = Sig/np.outer(d,d)
    iu = np.triu_indices_from(obs,1)
    return np.sqrt(np.mean((obs[iu]-imp[iu])**2))

print("="*60)
print("CFA: four-factor measurement model")
spec4 = "\n".join(f"{k} =~ "+" + ".join(v) for k,v in CONSTRUCTS.items())
m4,s4 = fit_cfa(spec4)
print(f"  chi2({int(s4['DoF'])}) = {s4['chi2']:.2f}   CFI={s4['CFI']:.3f}  TLI={s4['TLI']:.3f}  "
      f"RMSEA={s4['RMSEA']:.3f}  SRMR={srmr(m4):.3f}  AIC={s4['AIC']:.0f}")

print("\nCFA: one-factor (common method / Harman, ML)")
spec1 = "G =~ " + " + ".join(all_items)
m1,s1 = fit_cfa(spec1)
print(f"  chi2({int(s1['DoF'])}) = {s1['chi2']:.2f}   CFI={s1['CFI']:.3f}  TLI={s1['TLI']:.3f}  "
      f"RMSEA={s1['RMSEA']:.3f}  SRMR={srmr(m1):.3f}  AIC={s1['AIC']:.0f}")
print(f"  -> four-factor improves AIC by {s1['AIC']-s4['AIC']:.0f}; supports distinct constructs"
      if s4['AIC']<s1['AIC'] else "  -> one-factor not rejected")

# standardized loadings from 4-factor CFA
ins = m4.inspect(std_est=True)
load = ins[(ins['op']=='~') & (ins['rval'].isin(CONSTRUCTS.keys()))][['rval','lval','Est. Std']].copy()
load.columns=['construct','item','loading']
load['loading']=pd.to_numeric(load['loading'],errors='coerce')

print("\n"+"="*60)
print("Convergent validity: AVE and CR")
ave={}; cr={}
for c,its in CONSTRUCTS.items():
    L=load[load['construct']==c]['loading'].astype(float).values
    ave[c]=np.mean(L**2); cr[c]=(L.sum()**2)/(L.sum()**2 + np.sum(1-L**2))
    print(f"  {c:11s} AVE={ave[c]:.3f}  CR={cr[c]:.3f}  (AVE>=.50, CR>=.70)")

print("\nDiscriminant validity: Fornell-Larcker")
# factor correlations
cor = m4.inspect(std_est=True)
fc = cor[(cor['op']=='~~') & (cor['lval']!=cor['rval'])]
names=list(CONSTRUCTS)
FL=pd.DataFrame(np.eye(len(names)),index=names,columns=names)
for n in names: FL.loc[n,n]=np.sqrt(ave[n])
for _,r in fc.iterrows():
    a,b=r['lval'],r['rval']
    if a in names and b in names: FL.loc[a,b]=FL.loc[b,a]=float(r['Est. Std'])
print("  diagonal = sqrt(AVE); off-diagonal = factor correlation")
print(FL.round(3).to_string())

print("\nDiscriminant validity: HTMT")
R=df[all_items].corr().values
idx={it:k for k,it in enumerate(all_items)}
def mean_between(a,b):
    vals=[R[idx[x],idx[y]] for x in CONSTRUCTS[a] for y in CONSTRUCTS[b]]
    return np.mean(vals)
def mean_within(a):
    its=CONSTRUCTS[a]; vals=[R[idx[its[i]],idx[its[j]]] for i in range(len(its)) for j in range(i+1,len(its))]
    return np.mean(vals)
H=pd.DataFrame(index=names,columns=names,dtype=float)
for i,a in enumerate(names):
    for b in names[i+1:]:
        H.loc[a,b]=mean_between(a,b)/np.sqrt(mean_within(a)*mean_within(b))
print("  threshold: HTMT < .85 (strict) / .90 (liberal)")
print(H.round(3).to_string())

print("\n"+"="*60)
print("Full-collinearity VIF (CMB check): regress each construct mean on the others")
import numpy.linalg as la
means={c:df[its].mean(axis=1) for c,its in CONSTRUCTS.items()}
M=pd.DataFrame(means)
for c in names:
    y=M[c]; X=M.drop(columns=c).values; X=np.column_stack([np.ones(len(X)),X])
    b=la.lstsq(X,y,rcond=None)[0]; pred=X@b; r2=1-np.sum((y-pred)**2)/np.sum((y-y.mean())**2)
    print(f"  {c:11s} VIF={1/(1-r2):.2f}  (all < 3.3 indicates no serious CMB)")
