"""GEOG41160 Assignment 2, Question 1: Extension density by ED"""
"""Team: 5"""

#1.
#Election districts in Dublin: 162
#Applications for extensions to Dublin City Council between 2019-2025: 9,914

#2.
#Web mercator as a projected coordinate system that distorts land/water farther from the equator.
#We are working with point data which was in ESPG 3857, different from our EDs in ITM
#Because ITM is Ireland specific, and so is this project,  it is important to use that projection system
#Additionally, we can now do further analysis now that the feature layers are in same projection

#3.
#There are 14 applications that fall outside of EDs. This is because they fall along the boundary lines and are
#not read as "within" the geometry

#######################################
###STEP ZERO: getting paths and data###
#######################################

#This step sets up relative file paths and calls the data. It also connects the output folder where the geopackages, Duckdb, and any maps produced will be saved.

from pathlib import Path
import duckdb
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

###Setup
ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data"
PLANNING = DATA / "planning" / "planning_applications_national.gpkg"
EDS = DATA / "boundaries" / "eds_national.gpkg"
OUTPUT = ROOT / "outputs"
OUTPUT.mkdir(parents=True, exist_ok=True)
DATABASE = OUTPUT / "extensions.duckdb"

print("Working folder:", ROOT)

#########################################
###STEP ONE: DUCKDB and getting counts###
#########################################

#This step connects a duckdatabase and filters and cleans the data. Using SQL, we filter all eletion districts in Ireland to just those in Dublin/
#We also filter planning applications for 3 criteria: 1. Applications Dublin City Council, between 2019-2025, and including the word "extension"

###Connect to the DuckDB database
con = duckdb.connect(DATABASE)

###Load spatial tools
con.install_extension("spatial")
con.load_extension("spatial")

###Check 
print("Planning file exists:", PLANNING.exists())
print("ED boundaries file exists:", EDS.exists())

###Import the two national datasets into DuckDB
con.sql(f"CREATE OR REPLACE TABLE planning AS SELECT * FROM ST_Read('{PLANNING}')")
con.sql(f"CREATE OR REPLACE TABLE eds_national AS SELECT * FROM ST_Read('{EDS}')")

###Print the original row counts EDs
print("Total national electoral divisions:")
print(con.sql("SELECT COUNT(*) FROM eds_national"))

###Filter electoral divisions to Dublin City
con.sql("""
    CREATE OR REPLACE TABLE dublin_eds AS
    SELECT *
    FROM eds_national
    WHERE COUNTY_ENGLISH = 'DUBLIN CITY'
""")

print("Dublin City electoral divisions:")
print(con.sql("SELECT COUNT(*) FROM dublin_eds"))

###Print the orignal row counts for planning applications
print("Total national planning applications:")
print(con.sql("SELECT COUNT(*) FROM planning"))

###Filter planning applications to complete calendar years 2019–2025 (1/3)
con.sql("""
    CREATE OR REPLACE TABLE applications_2019_2025 AS
    SELECT *
    FROM planning
    WHERE year(ReceivedDate) BETWEEN 2019 AND 2025
""")

print("Applications received during 2019–2025:")
print(con.sql("SELECT COUNT(*) FROM applications_2019_2025"))

###Filter applications to Dublin City Council (2/3)
con.sql("""
    CREATE OR REPLACE TABLE dublin_applications AS
    SELECT *
    FROM applications_2019_2025
    WHERE PlanningAuthority = 'Dublin City Council'
""")

print("Applications from 2019-2025 to ONLY Dublin City Council:")
print(con.sql("SELECT COUNT(*) FROM dublin_applications"))

###Filter descriptions containing the word 'extension' (3/3) 
con.sql("""
    CREATE OR REPLACE TABLE extensions AS
    SELECT *
    FROM dublin_applications
    WHERE DevelopmentDescription COLLATE NOCASE
    LIKE '%extension%' 
""") #% allow the search to account for extention appearing WITHIN a larger text

print("Matching extension applications:")
print(con.sql("SELECT COUNT(*) FROM extensions"))

###Confirm the tables in the database
print("Tables in the database:")
print(con.sql("SHOW TABLES"))

###REPORTING VALUES###
#Election districts in Dublin: 162
#Applications for extensions to Dublin City Council between 2019-2025: 9,914

#########################################
###STEP TWO: Reproject CRS and Explain###
#########################################

#This step reprojects the point data from the housing applications into the ITM projection used by the election districts. ITM is the best projection system for Ireland
#so all data should be projected in ITM so further analysis is correct. 

###Read one feature from each source to check the CRS
dublin_eds_gdf = gpd.read_file(EDS, rows=1)
planning_gdf = gpd.read_file(PLANNING, rows=1)   #SQL was not doing this so briefly using python

###print crs of both features
print("Electoral divisions CRS:", dublin_eds_gdf.crs)
print("Planning applications CRS:", planning_gdf.crs)  #SQL was not doing this so briefly using python

###Electoral divisions
print(con.sql("""
    SELECT
        COUNT(*) AS features,
        ST_GeometryType(SHAPE) AS geometry_type
    FROM dublin_eds
    GROUP BY ST_GeometryType(SHAPE)
"""))

###Extension applications
print(con.sql("""
    SELECT
        COUNT(*) AS features,
        ST_GeometryType(SHAPE) AS geometry_type
    FROM extensions
    GROUP BY ST_GeometryType(SHAPE)
"""))

###Reproject
con.sql("""
    CREATE OR REPLACE TABLE extensions_itm AS
    SELECT
        * EXCLUDE (SHAPE),
        ST_Transform(
            SHAPE,
            'EPSG:3857',
            'EPSG:2157',
            always_xy := true
        ) AS SHAPE
    FROM extensions
""")

###REASONING FOR REPROJECT###
#Web mercator as a projected coordinate system that distorts land/water farther from the equator.
#We are working with point data which was in ESPG 3857, different from our EDs in ITM
#Because ITM is Ireland specific, and so is this project,  it is important to use that projection system
#Additionally, we can now do further analysis now that the feature layers are in same projection

#########################
###STEP THREE: Joining###
#########################

#This step joins the extensions point data to the EDs geography, checks for correct oporation, and counts the number of applications that fall outside of the EDS.
#This way we can calculate density per election district in the next step
#Because St_within excludes values (applications) that lay exactly on election district boundaries there may be excluded values. 
#This does not necessarily indicate errors in the dataset. 

###Joining 
con.sql("""
    CREATE OR REPLACE TABLE ed_counts AS
    SELECT
        eds.ED_ENGLISH,
        eds.SHAPE,
        COUNT(p.ApplicationNumber) AS applications
    FROM dublin_eds AS eds
    LEFT JOIN extensions_itm AS p
        ON ST_Within(p.SHAPE, eds.SHAPE)
    GROUP BY
        eds.ED_ENGLISH,
        eds.SHAPE
""")

###Checking
print(con.sql("""
    SELECT ED_ENGLISH, applications
    FROM ed_counts
    ORDER BY applications DESC
    LIMIT 10
"""))

###Counting applications that fell outside of EDs
print(con.sql("""
    SELECT COUNT(*) AS applications_outside_eds
    FROM extensions_itm AS p
    WHERE NOT EXISTS (
        SELECT 1
        FROM dublin_eds AS eds
        WHERE ST_Within(p.SHAPE, eds.SHAPE)
    )
"""))

###EXPLANATION###
#There are 14 applications that fall outside of EDs. This is because they fall along the boundary lines and are
#not read as "within" the geometry

##########################################
###STEP FOUR: Calculate Density and MAP###
##########################################

#This step combines the density calculation and map creation. 
#A map of the density of planning applications is created and exported to outputs, as well as a geopackage of the density stats that will be used for further analysis.

###Get EDs and geometries from DuckDB
df = con.sql("""
    SELECT
        ED_ENGLISH,
        applications,
        ST_AsWKB(SHAPE) AS wkb
    FROM ed_counts
""").df()

###Create GeoDataFrame
eds_map = gpd.GeoDataFrame(
    df.drop(columns="wkb"),
    geometry=gpd.GeoSeries.from_wkb(df["wkb"].apply(bytes)),
    crs="EPSG:2157")

###Calculate extension applications per km2
eds_map["per_km2"] = (eds_map["applications"] / (eds_map.geometry.area / 1e6))

###Plot the choropleth map
fig, ax = plt.subplots(figsize=(7, 6))

eds_map.plot(
    column="per_km2",
    scheme="Quantiles",
    k=5,
    cmap="Wistia",
    edgecolor="Black",
    linewidth=0.2,
    legend=True,
    legend_kwds={
        "title": "Extensions per km²",
        "fmt": "{:.0f}",
        "loc": "lower right"
    },
    ax=ax
)

ax.set_title("Density of Applications for Extensions, Dublin City, 2019–2025")
ax.set_axis_off()

###Save the map
png_path = OUTPUT / "ExtensionDensity_DublinED.png"
fig.savefig(png_path, dpi=180, bbox_inches="tight")
plt.show()
plt.close(fig)

###Saving Geopackage
eds_map.to_file(OUTPUT / "DublinED_ExtensionDensity.gpkg")
print(gpd.read_file(OUTPUT / "DublinED_ExtensionDensity.gpkg").head())
