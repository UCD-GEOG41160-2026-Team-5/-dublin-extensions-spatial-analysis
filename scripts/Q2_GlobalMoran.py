"""
GEOG41160 Assignment 2, Question 2: GLOBAL SPATIAL AUTOCORRELATION (5 MARKS).
Team: 5

ANSWERS
Question 2:
1. Distribution: skewness of the extension density is 1.38, so we used np.log1p transformation to handle zero values and right-skewness. 
                 A log transformation changes the distribution and scale of the variable, reducing the influence of extremely high values.
                      
2. Weights: QUEEN CONTIGUITY via libpysal.weights.Queen
            REASON: We used Queen contiguity because it defines neighbors as EDs that share either a border or a corner,
                    which is appropriate for the irregular shapes of Dublin's EDs.

3. Moran's I: Raw Data = 0.332 (p = 0.000: p<0.001); log1p 0.373 (p = 0.000: p<0.001), 9,999 permutations, seed 42. 

Interpretation:
RAW DATA MAP:
    Fom the map we saw that a few areas in Dublin have massive numbers of planning extensions (up to 400+).
    Because of these extreme high values, the color scale stretches out so much that almost the entire city turns a pale, washed-out yellow.
    It makes it look like nothing interesting is happening in most of Dublin, which isn't true.
    The raw data map is misleading because it hides the variation in extension density across most of the city,
    making it hard to identify meaningful patterns or clusters.

LOG-TRANSFORMED MAP:
    We noticed that the scale is much more balanced now. The log transformation tames those giant numbers so they don't dominate the map.
    It spreads the green shades out fairly across the city. This allows you to see the spatial variation more clearly, the transformation reduces the influence of extreme values, allowing differences between other areas to become more visible.

THE STATISTICAL RESULTS:
RAW DATA: Moran's I = 0.332  and p = 0.000(p < 0.001) Indicates significant positive spatial autocorrelation.
    The positive Moran's I value indicates that planning extensions in Dublin City are not random. Neighborhoods with high
    extension density naturally group together next to other high-density areas.
    The reported p-value of 0.000 (rounded to three decimal places) indicates strong statistical evidence against the null hypothesis of spatial randomness (p < 0.001).

LOG-TRANSFORMED DATA: Moran's I = 0.373 and p = 0.000 (p < 0.001): Indicates significant positive spatial autocorrelation.
    After rescaling the  raw data with  a log transformation, the  Moran's I value increased to 0.373, indicating  stronger spatial autocorrelation.
    The p-value remains below 0.001, confirming that this pattern is statistically significant and not random. 
    The log transformation reduced the influence of extreme valuesly high density values,
    allowing us to see the true spatial relationships in extension density across Dublin City.
    The overall conclusion remained the same: planning extension densities were spatially clustered, not randomly distributed. 

PATTERN:
    We found that the pattern of clustering is consistent between the raw and log-transformed data,
    but the log transformation map makes it easier to see the differences in extension density across Dublin City, providing a
    clearer visualization of the spatial distribution.

WHY THE LOG-TRANSFORMED DATA IS PREFERRED TO VISUALISE AND ANALYSE:
    We prefered the log-transformed data because it reduces the influence of extreme values, allowing differences between other areas to become more visible and 
    improves the distribution of colours on the map, providing a more honest visual picture of the spatial distribution of extension density across Dublin City.

Conclusion:
    Both datasets show significant positive spatial autocorrelation, although the transformed dataset has a higher Moran's I.
    The raw and the log-transformed data give a p-value of 0.000 (p < 0.001). This meant that  both maps agree that planning extensions in Dublin
    are significantly clustered, not random.

"""
###################################################################################################################################
############################################# SETUP #################################################################################
###################################################################################################################################

# For Question 2 part 1 we will need the following libaries.

from pathlib import Path
import numpy as np                         # handles numerical operations
import geopandas as gpd                    # handle the spatial vector data like the .gpkg output
import matplotlib.pyplot as plt            # using it because we needed to produce and histogram.
from scipy.stats import skew               # to calculate the  numerical skweness of the extension density.

# We then had define the paths based on the assignment script template.

ROOT = Path(__file__).resolve().parents[1]   # the repository folder
DATA = ROOT / "data"
OUTPUT = ROOT / "outputs"
OUTPUT.mkdir(exist_ok=True)
EXTENSION_DENSITY = OUTPUT / "DublinED_ExtensionDensity.gpkg"  # Saved from Question 1

# Safety Check: To ensure that Question 1 output exists before running the analysis.
if not EXTENSION_DENSITY.exists():
    raise FileNotFoundError(f"{EXTENSION_DENSITY} not found: please run Q1_ExtensionDensity.py first.")

# Load the spatial dataset produced in Question 1
eds = gpd.read_file(EXTENSION_DENSITY)
print(len(eds),"EDs,", eds.crs)
print(eds.columns) # to confirm if the  column is named Extension_density.  We confirmed that column was named per km2 not Extension_density 

#######################################################################################################################
############## 1.Check the distribution of extension density (histogram and skewness)####################################
#######################################################################################################################

#IMPORTANCE:
""" 
    Checking the distribution of extension density across Dublin City's Electoral Divisions (EDs)
    before calculating Moran's I is essential because the statistic relies on deviations from the mean. 
    It tells us if our values are unevenly spread out and its from  this that we can determine if 
    the data is normally distributed or skewed and transform it to make it more suitable for analysis if necessary.
"""

# step 1 of the question required us to check the distribution of the extension density 
raw_skew = skew(eds["per_km2"])
print("Raw data skewness: %.2f" % raw_skew)

# then plotting the  histogram to show if its strongly skewed.
plt.figure(figsize=(6, 4))
plt.hist(eds["per_km2"], bins=30, color="#4a7c3a")
plt.title(" Raw Data Skewness") 
plt.xlabel("Extensions per km2")
plt.ylabel("Number of Electoral Divisions")
plt.tight_layout()
plt.savefig( OUTPUT /"Raw_Histogram.png", dpi=300, bbox_inches="tight")
plt.show()

# After plotting we noticed that the histogram was strongly skewed.
"""
      This is because most of the EDs packed city center areas and have a low extension count due to limited space 
      unlike the outer suburban EDs  which have a high extension count accounting on the long right tall  hence  the need to transform it.
"""

# We had to apply log1p transformation to handle zero values and right-skewness
eds["log_density"] = np.log1p(eds["per_km2"])

# Then we had to print skewness comparison for raw vs log-transformed density
print("Skewness, raw: %.2f, log: %.2f" % (skew(eds["per_km2"]), skew(eds["log_density"])))

# Plot histograms to compare raw vs. log-transformed distributions
fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))

# Plotting the Raw data on the left side 
axes[0].hist(eds["per_km2"], bins=30, color="#4a7c3a")
axes[0].set_title("Raw Data")
axes[0].set_xlabel("Extension per Km2")
axes[0].set_ylabel("Number of Electoral Divisions")

# Plotting the Log transformed graph on the Right.
axes[1].hist(eds["log_density"], bins=30, color="#1f77b4")
axes[1].set_title(" Transformed Data")
axes[1].set_xlabel("log(1 + extensions per km2)")
axes[1].set_ylabel(" Number of Electoral Divisions")

plt.tight_layout()

# Saving the Histogram figure.
plt.savefig(OUTPUT / "DublinED_Raw_vs_LogTransformed_Distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# JUSTIFICATION.
""" Because Moran’s I is built on deviations from the mean, extreme values can dominate it.
    The first step is to check the distribution using a histogram and skewness statistic. 
    If the planning extension density is strongly lopsided, a log transformation is applied.
    np.log1p transformation to handle zero values and right-skewness.
    A log transformation changes the distribution and scale of the variable, reducing the influence of extremely high values.
"""
                      
######################################################################################################################
################## 2. SPATIAL WEIGHTS  ##############################################################################
########################################################################################################################

### EXPLANATION WHY THIS STEP?
"""""
    Calculating spatial weights is crucial because they translate geographic boundaries into a mathematical neighbor network,
    enabling Moran's I to test whether extension densities are truly clustered across Dublin City.
"""

#NEIGHBOURHOOD DEFINITION:
""" 
    NEIGHBOUR: QUEEN CONTIGUITY via libpysal.weights.Queen
    REASON: We used Queen contiguity because it defines neighbors as EDs that share either a border or a corner,
            which is appropriate for the irregular shapes of Dublin's EDs. 
"""

# First thing was we had to import ibaraires needed for this question.
from libpysal.weights import Queen

# We then had to build the spatial weights using Queen contiguity so that the EDs sharing a border or a corner are grouped as neighbors.
w = Queen.from_dataframe(eds, use_index=True)

#Print checks for isloated areas with zero neighbours and neighbor statistics
print("Islands:", w.islands)
print("Neighbours: min", w.min_neighbors, "mean", round(w.mean_neighbors, 1), "max", w.max_neighbors)

# Row-standardises the weightS so each ED’s weights add up to 1. 
w.transform = "r"

########################################################################################################################
######################################## 3. GLOBAL MORAN'S I ###########################################################
########################################################################################################################

# IMPORTANCE OF THIS STEP:
""" 
    Calculating Global Moran's I measures spatial autocorrelation to determine whether planning applications for residential extensions
    across Dublin's Electoral Divisions are systematically clustered, dispersed, or randomly distributed.
"""

# Importing the libaries needed for this section
from esda.moran import Moran

# Define the Settings
SEED = 42
PERMUTATIONS = 9999

   
# Compute Global Moran's I for Raw Density (per_km2)
np.random.seed(SEED)
Raw_Density  = eds["per_km2"].values
moran_raw = Moran(Raw_Density, w, permutations=PERMUTATIONS)

# Compute Global Moran's I for Log-Transformed Density (log_density) (Our Chosen Variable)
np.random.seed(SEED)
Transformed_Density = eds["log_density"].values
moran_log = Moran(Transformed_Density, w, permutations=PERMUTATIONS)

# The I and p-values for the raw density and the chosen variable(log_density)
# I and P values for raw density 
print("Moran's I: %.3f | p-value: %.3f" % (moran_raw.I, moran_raw.p_sim))

# I and P values for log_density
print("Moran's I: %.3f | p-value: %.3f" % (moran_log.I, moran_log.p_sim))

#########################################################################################################################################################
################################################# 4. INTERPRETING  THE RESULTS ###########################################################################
##########################################################################################################################################################
# INTERPRETATION OF THE RESULTS:
""""
    Before interpreting the results, we had to visualise the map because it lets us actually see where those high-density clusters are located across 
    Dublin City,unlike the numerical Moran's I value which only tells us the degree of clustering.
"""
# For visulation of the map i want to  compare  the log_density with the raw density to see if the log transformation has improved the spatial clustering of the extension density across Dublin City. And kmow why the log transformed is the prefered choice for the analysis.
from plotting_helpers import fix_colorbar_height  # had to import from week 7 work. A proper color bar ensures that the colors on your map accurately reflect what is happening on the ground. Without fixing it, your map tells a misleading visual story

# Create a figure with two side-by-side subplots on the same page
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Plotting the Raw Data on the left side of the figure

eds.plot(column="per_km2",ax=axs[0], cmap="YlGn", legend=True, edgecolor="grey", linewidth=0.3, legend_kwds={"label":"Raw Data"})

# Fix the colorbar height for the first map
fix_colorbar_height(fig, axs[0])

axs[0].set_title("Raw Data Map")
axs[0].set_axis_off()

# Map 2: Log-Transformed Data
eds.plot(column="log_density",
    ax=axs[1],
    cmap="YlGn",
    legend=True,
    edgecolor="grey",
    linewidth=0.3,
    legend_kwds={"label": "Transformed Density"},
)

# Fix the colorbar height for the second map
fix_colorbar_height(fig, axs[1])

axs[1].set_title(" Log-Transformed Map")
axs[1].set_axis_off()


# Finalise layout and save the figure
plt.tight_layout()
plt.savefig(OUTPUT / "Raw_vs_Transformed_Comparison.png", dpi=180, bbox_inches="tight")
plt.show()

# Explanation of the results: for the comparison image above

# RAW DATA MAP:
""" Fom the map we saw that a few areas in Dublin have massive numbers of planning extensions (up to 400+).
    Because of these extreme high values, the color scale stretches out so much that almost the entire city turns a pale, washed-out yellow.
    It makes it look like nothing interesting is happening in most of Dublin, which isn't true.
    The raw data map is misleading because it hides the variation in extension density across most of the city,
    making it hard to identify meaningful patterns or clusters.
"""
# LOG-TRANSFORMED MAP:
""" We noticed that the scale is much more balanced now. The log transformation tames those giant numbers so they don't dominate the map.
    It spreads the green shades out fairly across the city. This allows you to see the spatial variation more clearly, the transformation reduces the influence of extreme values, allowing differences between other areas to become more visible.
"""

# THE STATISTICAL RESULTS:
# RAW DATA: Moran's I = 0.332  and p = 0.000(p < 0.001) Indicates significant positive spatial autocorrelation.
""" The positive Moran's I value indicates that planning extensions in Dublin City are not random. Neighborhoods with high
    extension density naturally group together next to other high-density areas.
    The reported p-value of 0.000 (rounded to three decimal places) indicates strong statistical evidence against the null hypothesis of spatial randomness (p < 0.001).
"""

# LOG-TRANSFORMED DATA: Moran's I = 0.373 and p = 0.000 (p < 0.001): Indicates significant positive spatial autocorrelation.
""" After rescaling the  raw data with  a log transformation, the  Moran's I value increased to 0.373, indicating  stronger spatial autocorrelation.
    The p-value remains below 0.001, confirming that this pattern is statistically significant and not random. 
    The log transformation reduced the influence of extreme valuesly high density values,
    allowing us to see the true spatial relationships in extension density across Dublin City.
    The overall conclusion remained the same: planning extension densities were spatially clustered, not randomly distributed. 
"""
# FINAL TRANSFORMED DATA MAP
fig, ax = plt.subplots(figsize=(7, 6))
eds.plot(column="log_density", cmap="YlGn", legend=True, edgecolor="grey", linewidth=0.3, ax=ax, legend_kwds={"label": "Transformed Density"})
ax.set_title("Transformed Map of Extension Density, Dublin City")
ax.set_axis_off()

# Fix the colorbar height using your helper function
fix_colorbar_height(fig, ax)

# Save the output
plt.savefig(OUTPUT / "Log-Transformed_Map.png", dpi=180, bbox_inches="tight")
plt.show()
    
# PATTERN:
""" We found that the pattern of clustering is consistent between the raw and log-transformed data,
    but the log transformation map makes it easier to see the differences in extension density across Dublin City, providing a
    clearer visualization of the spatial distribution.
"""
# WHY THE LOG-TRANSFORMED DATA IS PREFERRED TO VISUALISE AND ANALYSE:
""" We prefered the log-transformed data because it reduces the influence of extreme values, allowing differences between other areas to become more visible and 
    improves the distribution of colours on the map, providing a more honest visual picture of the spatial distribution of extension density across Dublin City.
"""

# Conclusion:
""" Both datasets show significant positive spatial autocorrelation, although the transformed dataset has a higher Moran's I.
    The raw and the log-transformed data give a p-value of 0.000 (p < 0.001). This meant that  both maps agree that planning extensions in Dublin
    are significantly clustered, not random. 
"""
