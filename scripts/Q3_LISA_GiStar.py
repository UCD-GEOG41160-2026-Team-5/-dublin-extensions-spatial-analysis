"""
GEOG41160 Assignment 2, Question 3: Local Clusters and Hotspots (LISA & Getis-Ord Gi*)
Team: 5

ANSWERS
1. Preprocessing & Spatial Weights Justification:
   - Variable Consistency: Continued using log-transformed extension density (np.log1p) from Q2 to maintain analytical consistency and mitigate the distorting impact of extreme high values on local spatial statistics.
   - Neighborhood Structure: Constructed Queen contiguity weights across 162 Electoral Divisions (EDs), yielding an average of 5.7 neighbors per ED with 0 isolated islands (Islands = 0).
   - LISA Spatial Weights: Used row-standardized weights (transform='r', row sums = 1) to evaluate relative spatial lag across varying neighborhood sizes.
   - Gi* Spatial Weights: Used binary unstandardized weights (transform='B', 0/1 adjacency) paired with star=True to incorporate the focal observation's value into local sum calculations.

2. LISA Computation & Significance (Raw vs. FDR Corrected):
   - Permutations & Seed: Computed Local Moran's I with 9,999 Monte Carlo permutations (seed=42).
   - Raw Significance (p <= 0.05): 51 EDs were statistically significant, comprising 20 High-High, 23 Low-Low, 5 Low-High, and 3 High-Low. The remaining 111 EDs were classified as Not Significant.
   - FDR Correction (esda.fdr at alpha = 0.05): The critical p-value threshold is 6.17284e-04. Exactly 2 EDs remain statistically significant after FDR correction, both of which belong to the High-High (HH) category.

3. Getis-Ord Gi* Hotspot Analysis & Two-Sided FDR Correction:
   - Test Specification: Evaluated using two-sided pseudo p-values (alternative='two-sided').
   - Z-score & FDR Interpretation: Z-scores indicate the direction and magnitude of deviation from the spatial-randomness expectation (|Z| > 1.96), while FDR correction controls for multiple testing across EDs.
   - Empirical Results: Across all 162 EDs, the FDR critical p-value threshold is 3.08642e-04. Exactly 0 EDs pass FDR correction.
   - Post-FDR Classification: 0 Hotspots (Z > 1.96 AND FDR p <= threshold), 0 Coldspots (Z < -1.96 AND FDR p <= threshold), 162 Not Significant.

4. Comparison between LISA and Gi*:
   - Methodological Differences: LISA measures local spatial association between an ED and its spatial lag (identifying clusters HH/LL and spatial outliers HL/LH). Gi* measures local intensity concentration of high/low values within an ED and its neighbors (star=True).
   - Mapping Criteria: Per assignment brief instructions, the LISA map displays raw significance categories (Q3.1, p <= 0.05), whereas the Gi* map displays FDR-corrected hotspot classifications (Q3.4).
   - Empirical Comparison: Following FDR correction (alpha = 0.05), LISA detects 2 significant High-High local spatial associations, whereas Gi* detects 0 significant hotspots or coldspots. The differing outcomes reflect distinct underlying test statistics and multi-testing sensitivity rather than an analytical discrepancy.
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

#########################################
##### SETUP #####
#########################################

ROOT = Path(__file__).resolve().parents[1]      # repository base folder
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

SEED = 42                                       # fixed random seed
PERMUTATIONS = 9999                             # minimum 9999 permutations

INPUT_GPKG = OUTPUTS / "DublinED_ExtensionDensity.gpkg"

if not INPUT_GPKG.exists():
    raise FileNotFoundError(f"{INPUT_GPKG} not found: please run Q1_ExtensionDensity.py first.")

eds = gpd.read_file(INPUT_GPKG)
print(len(eds), "EDs loaded, CRS:", eds.crs)     # 162 EDs, EPSG:2157


#########################################
##### 1. Preprocessing & Spatial Weights #####
#########################################

# Log transformation to maintain consistency with Question 2 and reduce skewness
eds["log_density"] = np.log1p(eds["per_km2"])

# 1A. Queen spatial weights matrix for LISA (row-standardized)
w_lisa = Queen.from_dataframe(eds, use_index=True)
w_lisa.transform = "r"
print(f"LISA Queen spatial weights constructed (row-standardized). Mean neighbors: {w_lisa.mean_neighbors:.1f}, Islands: {len(w_lisa.islands)}")

# 1B. Separate Queen spatial weights matrix for Gi* (binary unstandardized)
w_gi = Queen.from_dataframe(eds, use_index=True)
w_gi.transform = "B"
print(f"Gi* Queen spatial weights constructed (binary unstandardized). Mean neighbors: {w_gi.mean_neighbors:.1f}, Islands: {len(w_gi.islands)}")


#########################################
##### 2. Local Moran's I (LISA) & FDR #####
#########################################

np.random.seed(SEED)
lm = Moran_Local(
    y=eds["log_density"].values,
    w=w_lisa,
    transformation="r",
    permutations=PERMUTATIONS,
    seed=SEED
)

# Raw p <= 0.05 classification for LISA Map (Q3.1)
labels = {1: "High-High", 2: "Low-High", 3: "Low-Low", 4: "High-Low"}
raw_sig_mask_lisa = (lm.p_sim <= 0.05)

eds["lisa_cluster"] = [
    labels[lm.q[i]] if raw_sig_mask_lisa[i] else "Not Significant"
    for i in range(len(eds))
]

print("\n--- LISA Analysis ---")
print(f"Raw significant EDs (p <= 0.05): {raw_sig_mask_lisa.sum()}")
print("LISA Cluster Distribution (Raw p <= 0.05):")
print(eds["lisa_cluster"].value_counts())

# Separate FDR Correction for LISA (Q3.2)
p_fdr_lisa = fdr(lm.p_sim, alpha=0.05)
if p_fdr_lisa is not None and not np.isnan(p_fdr_lisa) and p_fdr_lisa > 0:
    fdr_sig_lisa = (lm.p_sim <= p_fdr_lisa)
    print(f"FDR critical p-value threshold: {p_fdr_lisa:.5e}")
    print(f"EDs remaining significant after FDR correction: {fdr_sig_lisa.sum()}")
    
    # Category breakdown for FDR-significant EDs (2 HH EDs)
    fdr_lisa_labels = [labels[lm.q[i]] if fdr_sig_lisa[i] else "Not Significant" for i in range(len(eds))]
    fdr_counts = pd.Series(fdr_lisa_labels).value_counts()
    print("Post-FDR Category Breakdown:")
    print(fdr_counts[fdr_counts.index != "Not Significant"])
else:
    print("FDR critical p-value threshold: None passed FDR at alpha=0.05")
    print("EDs remaining significant after FDR correction: 0")

# Plot LISA Cluster Map (Q3.3)
color_map_lisa = {
    "High-High": "#d73027",        # Red
    "Low-Low": "#4575b4",          # Blue
    "High-Low": "#fdae61",         # Light Orange
    "Low-High": "#abd9e9",         # Light Blue
    "Not Significant": "#e0e0e0"   # Light Grey
}

fig, ax = plt.subplots(figsize=(8, 7))
eds.plot(
    color=[color_map_lisa[c] for c in eds["lisa_cluster"]],
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
print(f"LISA map successfully saved to: {lisa_png}")
plt.show()


#########################################
##### 3. Getis-Ord Gi* & Two-Sided FDR #####
#########################################

np.random.seed(SEED)
gi = G_Local(
    y=eds["log_density"].values,
    w=w_gi,
    transform="B",
    star=True,
    permutations=PERMUTATIONS,
    seed=SEED,
    alternative="two-sided"
)

# Gi* uses two-sided pseudo p-values (gi.p_sim)
p_fdr_gi = fdr(gi.p_sim, alpha=0.05)

if p_fdr_gi is not None and not np.isnan(p_fdr_gi) and p_fdr_gi > 0:
    gi_fdr_mask = (gi.p_sim <= p_fdr_gi)
    print(f"\n--- Getis-Ord Gi* Analysis ---")
    print(f"FDR critical p-value threshold for Gi*: {p_fdr_gi:.5e}")
    print(f"EDs remaining significant after FDR correction: {gi_fdr_mask.sum()}")
else:
    gi_fdr_mask = np.zeros(len(eds), dtype=bool)
    print(f"\n--- Getis-Ord Gi* Analysis ---")
    print("FDR critical p-value threshold for Gi*: None passed FDR at alpha=0.05")
    print("EDs remaining significant after FDR correction: 0")

# Classify Hotspots (Z > 1.96 AND FDR sig) and Coldspots (Z < -1.96 AND FDR sig)
gi_labels = []
for i in range(len(eds)):
    if gi_fdr_mask[i]:
        if gi.Zs[i] > 1.96:
            gi_labels.append("Hotspot (Z > 1.96)")
        elif gi.Zs[i] < -1.96:
            gi_labels.append("Coldspot (Z < -1.96)")
        else:
            gi_labels.append("Not Significant")
    else:
        gi_labels.append("Not Significant")

eds["gi_star"] = gi_labels

print("Gi* Hotspot Distribution (FDR corrected, Z > 1.96 / Z < -1.96):")
print(eds["gi_star"].value_counts())

# Plot Getis-Ord Gi* Map (Diverging Color Scheme - Q3.5)
color_map_gi = {
    "Hotspot (Z > 1.96)": "#d73027",    # Red
    "Coldspot (Z < -1.96)": "#4575b4",   # Blue
    "Not Significant": "#e0e0e0"         # Light Grey
}

fig, ax = plt.subplots(figsize=(8, 7))
eds.plot(
    color=[color_map_gi[c] for c in eds["gi_star"]],
    edgecolor="white",
    linewidth=0.3,
    ax=ax
)

# 确保在地图图例中始终保留全部三种类别说明，清晰展示作业要求的 Diverging Color Scheme
legend_gi = [
    Patch(facecolor=color, edgecolor="grey", label=label)
    for label, color in color_map_gi.items()
]
ax.legend(handles=legend_gi, loc="lower right", title="Gi* Category (FDR p-val & |Z| > 1.96)")
ax.set_title("Getis-Ord Gi* Hotspot Analysis (Dublin City)")
ax.set_axis_off()

gi_png = OUTPUTS / "GiStar_ExtensionDensity_DublinED.png"
fig.savefig(gi_png, dpi=300, bbox_inches="tight")
print(f"Gi* hotspot map successfully saved to: {gi_png}")
plt.show()