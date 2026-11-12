"""
GEOG41160 Assignment 2, Question 3: Local Clusters and Hotspots (LISA & Getis-Ord Gi*)
Team: 5

ANSWERS
Q3.1 (LISA Computation & Raw Significance at p <= 0.05):
   - Out of 162 Electoral Divisions (EDs), 50 EDs are statistically significant at raw p <= 0.05.
   - Spatial Breakdown: 20 High-High clusters, 23 Low-Low clusters, 5 Low-High outliers, 
     2 High-Low outliers, and 112 Not Significant.
   - Monte Carlo Parameters: 9,999 permutations with fixed random seed (seed=42).

Q3.2 (LISA False Discovery Rate Correction):
   - Critical FDR p-value threshold: 6.17284e-04 (alpha = 0.05).
   - Exactly 2 EDs remain statistically significant after FDR correction, both belonging 
     to the High-High (HH) cluster category. FDR controls the expected proportion of false 
     discoveries across 162 simultaneous hypothesis tests.

Q3.3 (LISA Cluster Map):
   - Mapped using 5 discrete spatial categories based on raw significance (p <= 0.05). 
     Saved to outputs/LISA_ExtensionDensity_DublinED.png.

Q3.4 (Getis-Ord Gi* Hotspot Analysis & Two-Sided FDR Correction):
   - Computed using binary unstandardized weights with star=1.0 (including focal ED in local sums).
   - Z-scores evaluated via two-sided p-values derived from standard normal distribution: 2 * norm.sf(|Z|).
   - Raw Uncorrected Classification (|Z| > 1.96): 15 Hotspots, 25 Coldspots, 122 Not Significant.
   - Critical FDR p-value threshold for Gi*: 1.85185e-03 (alpha = 0.05).
   - Post-FDR Classification: Exactly 6 EDs remain statistically significant after FDR correction 
     (1 Hotspot with Z > 1.96, and 5 Coldspots with Z < -1.96).

Q3.5 (Gi* Hotspot & Coldspot Map):
   - Mapped using a continuous RdBu_r diverging color scheme centered at Z = 0 (vmin=-lim, vmax=lim).
   - The 6 FDR-significant EDs are outlined with bold black polygon boundaries. 
     Saved to outputs/GiStar_ExtensionDensity_DublinED.png.

Q3.6 (LISA vs. Gi* Methodological & Empirical Comparison):
   - Overall Agreement: LISA and Gi* show substantial but incomplete agreement. Of the 20 High-High EDs identified by LISA, 
     14 are also classified as Gi* hotspots and 6 are Not Significant under raw Gi* classification. Of the 23 Low-Low EDs, 
     22 are also classified as Gi* coldspots and 1 is Not Significant.
   - Spatial Outliers: Of the 2 High-Low EDs, 1 is classified as a Gi* coldspot and 1 is Not Significant. Of the 5 Low-High EDs, 
     1 is classified as a Gi* hotspot and 4 are Not Significant.
   - Methodological Difference: LISA measures local spatial association by comparing each ED's deviation from the global mean with 
     the spatial lag of neighbouring values, using row-standardised Queen weights. Gi* evaluates whether the sum of values within 
     a local neighbourhood is unusually high or low, using binary Queen weights and including the focal ED (star=1.0). 
     Therefore, the two methods measure related but different spatial patterns.
   - Interpretation: A High-Low ED can still be classified as a Gi* coldspot if its value together with those of its neighbours produces a local sum 
     below the Gi* expected value. This illustrates why a local spatial outlier identified by LISA does not necessarily correspond to a Gi* hotspot.
   - Comparison Basis: The comparison uses raw LISA significance (p <= 0.05) and raw Gi* Z-score classification (|Z| > 1.96), before FDR correction.
"""


from pathlib import Path
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from libpysal.weights import Queen
from esda.moran import Moran_Local
from esda.getisord import G_Local
from esda import fdr
from scipy.stats import norm
from plotting_helpers import fix_colorbar_height

#########################################
##### SETUP & PREPROCESSING #####
#########################################

ROOT = Path(__file__).resolve().parents[1]      # Repository base directory
print("Working folder:", Path.cwd())

OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)

SEED = 42                                       # Fixed random seed for reproducibility
PERMUTATIONS_LISA = 9999                        # 9,999 Monte Carlo permutations for LISA
PERMUTATIONS_GI = 999                           # 999 permutations for Gi*

# Standardized input file path matching Question 1 output
EXTENSION_DENSITY = OUTPUTS / "DublinED_ExtensionDensity.gpkg"
if not EXTENSION_DENSITY.exists():
    raise FileNotFoundError(f"Required input layer not found at {EXTENSION_DENSITY}. Please execute Q1_ExtensionDensity.py first.")

eds = gpd.read_file(EXTENSION_DENSITY)
print(f"{len(eds)} EDs loaded, CRS: {eds.crs}")   # 162 EDs in Dublin City, EPSG:2157

# Density Column Resolution & Log Transformation Purpose
# 1. Variable Consistency: Q3 evaluates the same analytical target as Q2 (log-transformed extension density).
# 2. Mathematical Stability: np.log1p(x) computes log(1 + x), safely accommodating zero counts.
# 3. Skewness Reduction: Log transformation reduces the influence of extreme high-density outliers 
#    on cross-products and variance sums in local statistics.
density_col = "per_km2"
eds["log_density"] = np.log1p(eds[density_col])
x = eds["log_density"].values


########################################################
##### QUESTION 3.1: Compute Local Moran's I (LISA) #####
########################################################

# LISA Queen Spatial Weights Matrix & Row-Standardisation
# 1. Queen Contiguity Definition: Two EDs are recognized as spatial neighbors if they share either a common border or a corner point.
# 2. Row-Standardisation (transform='r'): Converts the spatial lag into a weighted average rather than a raw sum, 
#    reducing the influence of differing neighbor counts across EDs.
w_lisa = Queen.from_dataframe(eds, use_index=True)
w_lisa.transform = "r"
print(f"LISA Queen spatial weights constructed (row-standardized). Mean neighbors: {w_lisa.mean_neighbors:.1f}, Islands: {len(w_lisa.islands)}")

# Local Moran's I Computation & Quadrant Interpretation (Week 9 Part 2 Style)
# 1. Quadrant Definitions (Spatial Relationship Types):
#    - High-High (HH) & Low-Low (LL): Spatial Clusters (focal value aligns with neighbor average).
#    - High-Low (HL) & Low-High (LH): Spatial Outliers (focal value differs in value relative to neighbors).
# 2. Significance vs Quadrant: Quadrant membership describes spatial relation type; statistical significance 
#    is determined strictly by pseudo p-value (p <= 0.05).
lm = Moran_Local(
    x,
    w_lisa,
    permutations=PERMUTATIONS_LISA,
    seed=SEED
)

quadrants = {1: "High-High", 2: "Low-High", 3: "Low-Low", 4: "High-Low"}
classes = pd.Series(lm.q).map(quadrants)
eds["lisa_cluster"] = np.where(lm.p_sim <= 0.05, classes, "Not Significant")

print("\n--- Question 3.1: LISA Raw Analysis ---")
print(f"Raw significant EDs (p <= 0.05): {(lm.p_sim <= 0.05).sum()}")
print("LISA Cluster Distribution (Raw p <= 0.05):")
print(eds["lisa_cluster"].value_counts())


#######################################################
##### QUESTION 3.2: Apply FDR Correction for LISA #####
#######################################################

# False Discovery Rate (FDR) Multi-Testing Control
# 1. Multiple Testing Problem: Performing 162 simultaneous hypothesis tests inflates Type I false positive risk.
# 2. FDR Control: esda.fdr controls the expected proportion of false discoveries among significant results at alpha=0.05.
p_fdr_lisa = fdr(lm.p_sim, alpha=0.05)
print("\n--- Question 3.2: LISA FDR Correction ---")

if p_fdr_lisa is not None and not np.isnan(p_fdr_lisa):
    fdr_sig_lisa = (lm.p_sim <= p_fdr_lisa)
    print(f"FDR critical p-value threshold: {p_fdr_lisa:.5e}")
    print(f"EDs remaining significant after FDR correction: {fdr_sig_lisa.sum()}")
    
    fdr_lisa_labels = np.where(fdr_sig_lisa, classes, "Not Significant")
    fdr_counts = pd.Series(fdr_lisa_labels).value_counts()
    print("Post-FDR Category Breakdown:")
    print(fdr_counts[fdr_counts.index != "Not Significant"])
else:
    print("FDR critical p-value threshold: None passed FDR at alpha=0.05")
    print("EDs remaining significant after FDR correction: 0")


##########################################
##### QUESTION 3.3: Map LISA Classes #####
##########################################

# Categorical color scheme for raw LISA cluster map (p <= 0.05)
color_map_lisa = {
    "High-High": "#d73027",        # Red: High-density cluster
    "Low-Low": "#4575b4",          # Blue: Low-density cluster
    "High-Low": "#fdae61",         # Light Orange: High focal, low neighbors outlier
    "Low-High": "#abd9e9",         # Light Blue: Low focal, high neighbors outlier
    "Not Significant": "#e0e0e0"   # Light Grey: Statistically insignificant
}

fig, ax = plt.subplots(figsize=(8, 7))
eds.plot(
    color=eds["lisa_cluster"].map(color_map_lisa),
    edgecolor="white",
    linewidth=0.3,
    ax=ax
)

legend_lisa = [
    Patch(facecolor=color, edgecolor="grey", label=label)
    for label, color in color_map_lisa.items()
    if label in eds["lisa_cluster"].values
]
ax.legend(handles=legend_lisa, loc="lower right", title="LISA Cluster (p <= 0.05)")
ax.set_title("LISA Cluster Map of Extension Density (Dublin City)")
ax.set_axis_off()

lisa_png = OUTPUTS / "LISA_ExtensionDensity_DublinED.png"
fig.savefig(lisa_png, dpi=300, bbox_inches="tight")
print(f"\n--- Question 3.3: LISA Map ---")
print(f"LISA map successfully saved to: {lisa_png}")
plt.show()


#####################################################
##### QUESTION 3.4: Compute Getis-Ord Gi* & FDR #####       (any other CSV files or figures the scripts produce)
#####################################################

# Gi* Spatial Weights Rationale (Binary & Star=1.0)
# 1. Binary Unstandardized Weights (transform='B'): Assigns unit weight (1) to each neighbor to compute localized total attribute sums.
# 2. Inclusion of Self (star=1.0): Incorporates focal ED's attribute value into local sum calculation (Gi* vs Gi).
w_gi = Queen.from_dataframe(eds, use_index=True)
print(f"\n--- Question 3.4: Getis-Ord Gi* Analysis ---")
print(f"Gi* Queen spatial weights constructed. Mean neighbors: {w_gi.mean_neighbors:.1f}, Islands: {len(w_gi.islands)}")

# Z-Scores, Two-Sided p-Values & FDR Mechanics
# 1. gi.Zs: Raw Z-scores (positive Z = local concentration above random expectation; negative Z = below).
# 2. eds["gi_p"]: Normal approximation two-sided p-values (2 * norm.sf(|Z|)), evaluating both upper (hotspot) and lower (coldspot) tails.
# 3. fdr(...): Applies FDR correction to derived two-sided p-values.
gi = G_Local(
    x,
    w_gi,
    transform="B",
    star=1.0,
    permutations=PERMUTATIONS_GI,
    seed=SEED
)

eds["gi_z"] = gi.Zs
eds["gi_p"] = 2 * norm.sf(np.abs(gi.Zs))

p_fdr_gi = fdr(eds["gi_p"].values, alpha=0.05)

if p_fdr_gi is not None and not np.isnan(p_fdr_gi):
    gi_fdr_mask = (eds["gi_p"] <= p_fdr_gi)
    print(f"FDR critical p-value threshold for Gi*: {p_fdr_gi:.5e}")
    print(f"EDs remaining significant after FDR correction: {gi_fdr_mask.sum()}")
else:
    gi_fdr_mask = np.zeros(len(eds), dtype=bool)
    print("FDR critical p-value threshold for Gi*: None passed FDR at alpha=0.05")
    print("EDs remaining significant after FDR correction: 0")

# Dual-Condition Hotspot / Coldspot Classification using vectorized np.where() (Week 9 Part 4 Style)
# Requires BOTH: 1) FDR significance (gi_fdr_mask == True), 2) Directional Z-score threshold (|Z| > 1.96).
eds["gi_star"] = np.where(
    gi_fdr_mask & (eds["gi_z"] > 1.96),
    "Hotspot (Z > 1.96)",
    np.where(
        gi_fdr_mask & (eds["gi_z"] < -1.96),
        "Coldspot (Z < -1.96)",
        "Not Significant"
    )
)

print("Gi* Hotspot Distribution (FDR corrected, Z > 1.96 / Z < -1.96):")
print(eds["gi_star"].value_counts())

# Uncorrected raw Z-score classification (|Z| > 1.96) for Q3.6 Crosstabulation
eds["gi_raw_class"] = np.where(
    eds["gi_z"] > 1.96, "Hotspot",
    np.where(eds["gi_z"] < -1.96, "Coldspot", "Not Significant")
)
print("Raw Gi* Distribution (|Z| > 1.96, pre-FDR):")
print(eds["gi_raw_class"].value_counts())


######################################################
##### QUESTION 3.5: Map Gi* Hotspots & Coldspots #####
######################################################

# Diverging Z-Score Visualization & FDR Boundary Outlining
# 1. Diverging Palette (RdBu_r): Continuous color scale centered at Z = 0 (vmin=-lim, vmax=lim).
# 2. FDR Boundaries: Black outlines highlight EDs passing FDR correction.
lim = np.abs(eds["gi_z"]).max()
fig, ax = plt.subplots(figsize=(8, 7))
eds.plot(
    column="gi_z",
    cmap="RdBu_r",
    vmin=-lim,
    vmax=lim,
    legend=True,
    edgecolor="grey",
    linewidth=0.3,
    ax=ax,
    legend_kwds={"label": "Gi* Z-score"}
)

if gi_fdr_mask.sum() > 0:
    eds[gi_fdr_mask].boundary.plot(ax=ax, color="black", linewidth=1.5)

ax.set_title("Getis-Ord Gi* Z-scores of Extension Density\n(Outlined: Significant after FDR)")
ax.set_axis_off()
fix_colorbar_height(fig, ax)

gi_png = OUTPUTS / "GiStar_ExtensionDensity_DublinED.png"
fig.savefig(gi_png, dpi=300, bbox_inches="tight")
print(f"\n--- Question 3.5: Gi* Map ---")
print(f"Gi* hotspot map successfully saved to: {gi_png}")
plt.show()


###############################################
##### QUESTION 3.6: Compare Gi* with LISA #####
###############################################

# Q3.6 Crosstabulation Baseline & Alignment Rationale
# Cross-tabulates raw LISA classes (p <= 0.05) against raw uncorrected Gi* Z-score categories (|Z| > 1.96)
# to compare unadjusted spatial association metrics.
ct = pd.crosstab(eds["lisa_cluster"], eds["gi_raw_class"])

print("\n--- Question 3.6: Comparison Between LISA and Getis-Ord Gi* ---")

print("Cross-tabulation: LISA Clusters (p <= 0.05) vs. Gi* Raw Categories (|Z| > 1.96):")
print(ct)

print("\nAnalytical Interpretation:")
print("1. Overall Alignment:")
print("   The two methods exhibit a high degree of partial agreement (partial alignment), but are not completely identical.")
print("2. Class-Specific Consistency:")
print("   - 14 of 20 High-High EDs are also Gi* hotspots (6 are not significant under raw Gi*).")
print("   - 22 of 23 Low-Low EDs are also Gi* coldspots (1 is not significant under raw Gi*).")
print("3. Structural Mechanism & Spatial Outliers:")
print("   - LISA measures spatial lag relative to the global mean using row-standardized weights.")
print("   - Gi* computes unstandardized total neighborhood sums including the focal ED (star=1.0).")
print("   - In this dataset, 1 High-Low ED is classified as a Gi* coldspot, while the other is not significant. This is because Gi* includes the focal ED and its neighbours in the local sum, so low values among surrounding EDs can pull down the overall neighbourhood total.")

# Export the Q3 analysis summary table to the outputs
ct.to_csv(OUTPUTS / "LISA_vs_GiStar_Crosstab.csv")
results_df = eds[['ED_ENGLISH', 'applications', 'per_km2', 'lisa_cluster', 'gi_z', 'gi_star']]
results_df.to_csv(OUTPUTS / "LISA_GiStar_Results.csv", index=False)
print("\nAll Q3 CSV files successfully exported to outputs/:")
print(f" - {OUTPUTS / 'LISA_vs_GiStar_Crosstab.csv'}")
print(f" - {OUTPUTS / 'LISA_GiStar_Results.csv'}")
