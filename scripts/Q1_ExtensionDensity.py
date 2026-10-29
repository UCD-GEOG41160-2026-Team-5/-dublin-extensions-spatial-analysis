#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Replace the temporary JupyterLab path with ROOT = Path(__file__).resolve().parents[1].


# In[4]:


#########################
#########################  woooooohoooooooooo
######QUESTION ONE#######
#########################
#########################

#######################################
###STEP ZERO: getting paths and data###
#######################################
from pathlib import Path
import duckdb

# Temporary paths for JupyterLab testing (DO NOT FORGET IF YOU SEE THIS IT IS NOT RIGHT YET)
ROOT = Path.home() / "Downloads" / "dublin-extensions-spatial-analysis"
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)

PLANNING = DATA / "planning" / "planning_applications_national.gpkg"
EDS = DATA / "boundaries" / "eds_national.gpkg"

###Connect to the DuckDB database
con = duckdb.connect(str(OUTPUTS / "extensions.duckdb"))

###Load spatial tools
con.execute("INSTALL spatial")
con.execute("LOAD spatial")

###Check 
print("Planning file exists:", PLANNING.exists())
print("ED boundaries file exists:", EDS.exists())

#########################################
###STEP ONE: DUCKDB and getting counts###
#########################################

###Import the two national datasets into DuckDB

con.sql(f"""
    CREATE OR REPLACE TABLE planning AS
    SELECT *
    FROM ST_Read('{PLANNING}')
""")

con.sql(f"""
    CREATE OR REPLACE TABLE eds_national AS
    SELECT *
    FROM ST_Read('{EDS}')
""")

###Print the original row counts EDs

print("\nTotal national electoral divisions:")
print(con.sql("SELECT COUNT(*) FROM eds_national"))

###Filter electoral divisions to Dublin City

con.sql("""
    CREATE OR REPLACE TABLE dublin_eds AS
    SELECT *
    FROM eds_national
    WHERE COUNTY_ENGLISH = 'DUBLIN CITY'
""")

print("\nDublin City electoral divisions:")
print(con.sql("SELECT COUNT(*) FROM eds"))

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

print("\nApplications received during 2019–2025:")
print(con.sql("SELECT COUNT(*) FROM applications_2019_2025"))

###Filter applications to Dublin City Council (2/3)

con.sql("""
    CREATE OR REPLACE TABLE dublin_applications AS
    SELECT *
    FROM applications_2019_2025
    WHERE UPPER(TRIM(PlanningAuthority)) = 'DUBLIN CITY COUNCIL'
""")

print("\nApplications received by Dublin City Council in 2019–2025:")
print(con.sql("SELECT COUNT(*) FROM dublin_applications"))

###Filter descriptions containing the word 'extension' (3/3) 

con.sql(r"""
    CREATE OR REPLACE TABLE extensions AS
    SELECT *
    FROM dublin_applications
    WHERE regexp_matches(
        DevelopmentDescription,
        '(?i)\bextension\b'
    )
""")

print("\nMatching extension applications:")
print(con.sql("SELECT COUNT(*) FROM extensions"))

###Confirm the tables in the database

print("\nTables in the database:")
print(con.sql("SHOW TABLES"))

###REPORTING VALUES###
#Election districts in Dublin: 162
#Applications for extensions to Dublin City Council between 2019-2025: 9,657


# In[7]:


#########################################
###STEP TWO: Reproject CRS and Explain###
#########################################

###Read one feature from each source to check the CRS
import geopandas as gpd

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


# In[10]:


#########################
###STEP THREE: Joining###
#########################

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
print
(con.sql("""
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


# In[15]:


##################################
###STEP FOUR: Calculate Density###
##################################

con.sql("""
    CREATE OR REPLACE TABLE ed_density AS
    SELECT
        ED_ENGLISH,
        SHAPE,
        applications,
        ST_Area(SHAPE) / 1000000.0 AS area_km2,
        applications / (ST_Area(SHAPE) / 1000000.0)
            AS extensions_per_km2
    FROM ed_counts
""")

### Check the results
print(con.sql("""
    SELECT
        ED_ENGLISH,
        applications,
        ROUND(area_km2, 3) AS area_km2,
        ROUND(extensions_per_km2, 2) AS extensions_per_km2
    FROM ed_density
    ORDER BY extensions_per_km2 DESC
    LIMIT 10
"""))

###Do these numbers make sense?
print(con.sql("""
    SELECT
        ROUND(MIN(ST_Area(SHAPE) / 1000000.0), 3) AS smallest_ed_km2,
        ROUND(AVG(ST_Area(SHAPE) / 1000000.0), 3) AS mean_ed_km2,
        ROUND(MAX(ST_Area(SHAPE) / 1000000.0), 3) AS largest_ed_km2
    FROM dublin_eds
""")) #yes they do

###Save as geopackage
output_gpkg = OUTPUTS / "DublinED_ExtensionDensity.gpkg"

con.sql(f"""
    COPY (
        SELECT *
        FROM ed_density
    )
    TO '{output_gpkg.as_posix()}'
    WITH (
        FORMAT GDAL,
        DRIVER 'GPKG',
        LAYER_NAME 'DublinED_ExtensionDensity'
    )
""")

print("Saved! Bada-bing bada-boom:", output_gpkg)


# In[28]:


#########################
###STEP FIVE: Plotting###
#########################

import geopandas as gpd
import matplotlib.pyplot as plt

### Retrieve EDs and geometries from DuckDB
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
    crs="EPSG:2157"
)

###Calculate extension applications per km²
eds_map["per_km2"] = (
    eds_map["applications"] / (eds_map.geometry.area / 1e6)
)

###Plot the choropleth map
ax = eds_map.plot(
    column="per_km2",
    scheme="Quantiles",
    k=5,
    cmap="Wistia",
    edgecolor="Black",
    linewidth=0.2,
    figsize=(7, 6),
    legend=True,
    legend_kwds={
        "title": "Extensions per km²",
        "fmt": "{:.0f}",
        "loc": "lower right"
    }
)

ax.set_title(
    "Density of Applications for Extensions, Dublin City, 2019–2025"
)
ax.set_axis_off()

###Save the map
plt.savefig(
    OUTPUTS / "ExtensionDensity_DublinED.png",
    dpi=180,
    bbox_inches="tight"
)

plt.show()


# In[ ]:




