# GEOG41160 - PYTHON FOR GIS ASSIGNMENT 2

###############################################################################################################################################################################################TEAM 5 README##########################################################

**MODULE:**                    GEOG41160-PYTHON FOR GIS
**PROJECT:**                   SPATIAL AUTOCORRELLATION & HOTSPOT ANALYSIS
**TEAM:**                      TEAM 5
**GitHUB REPOSITORY:**         -dublin-extensions-spatial-analysis

## Overview
In this task we wrote a collaborative Python workflow that analysed where people in Dublin City extend their buildings based on the density of planning applications for extensions by Electoral Division (ED),performed global spatial autocorrelation, and analysed local clusters and hotspots across one shared Python codebase with each person's contribution visible in the Git history.

## README.md PURPOSE
The README.md file serves as the main documentation page for this repository, providing a clear overview of the team's project structure, spatial methodology, and collaborative workflow. It outlines the modular organization of Python scripts across assignment tasks (Q1_ExtensionDensity.py, Q2_GlobalMoran.py, and Q3_LISA_GiStar.py), local dataset directory structures, and data provenance for national spatial layers from data.gov.ie (CC BY 4.0). Additionally, it details the technical justification for standardizing spatial layers to Irish Transverse Mercator (EPSG:2157), .gitignore rules for excluding local data folders (data/) and temporary files, step-by-step terminal execution commands for seamless reproducibility, and a shared sprint log tracking project progress from Sprint 0 through Sprint 3. it has the script execution order

## Repository structure
A repository structure is an organised layout of folders in our team project, working like a Adigital  filing cabinet to ensure effortless navigation and code execution. Our repository structure combines setup documentation and the embedded sprint (README.md), sprint log and a version control rules (.gitignore) with local data storage (data/, scripts/, outputs/) and our python scripts for Q1_ExtensionDensity.py, Q2_GlobalMoran.py, and Q3_LISA_GiStar.py

# DATA FOLDER CONTENT
* **data:**      It contains the  planning_applications_national.gpkg and the eds_national.gpkg used in the project.
* **scripts:**   It contains the project's modular Python scripts (Q1_ExtensionDensity.py, Q2_GlobalMoran.py, and Q3_LISA_GiStar.py) and plotting_helpers.py for spatial analysis and mapping
* **outputs:**   It contains all generated spatial outputs, including the processed GeoPackage,map figures and exploratory histogram charts.

## DATA SOURCE, LICENCE, DATE AND CRS
* **PLANNING APPLICATONS DATA**
**Description:** Merged Planning Registers of participating Irish Local Authorities, including all planning applications received since 2012. Used as the primary raw spatial dataset from which Dublin extension applications are extracted.
**Publisher**: Department of Housing, Local Government and Heritage
**Source URL:** https://data-housinggovie.opendata.arcgis.com/datasets/housinggovie::planning-application-points/explore?location=53.754996%2C-6.834285%2C14
**Date of Download:** 10/27/2026
**Dataset:** Feature Layer
**LICENCE** Creative Commons Attribution 4.0 International (CC BY 4.0)
**File Path**: data/planning/planning_applications_national.gpkg
**ORIGINAL CRS:**  EPSG:3857

* **ELECTORAL DIVISONS**
**Description** CSO Electoral Divisions - National Statistical Boundaries - 2022 - Ungeneralised. National boundary dataset containing all 3,420 Electoral Divisions in Ireland, used to filter Dublin City boundaries and calculate local extension density.
The data was ungeneralised dataset, this means the boundary geometries are maintained at their highest level of precision and detail, without any smoothing, simplification, or removal of coordinates.
**Publisher**Tailte Éireann (Tailte Eireann MapGenie)
**Source URL:**https://data-osi.opendata.arcgis.com/datasets/osi::cso-electoral-divisions-national-statistical-boundaries-2022-ungeneralised/explore?location=47.748244%2C-20.583194%2C4
**Date of Download:** 10/27/2026
**Dataset:** Feature Layer
**LICENCE**  Creative Commons Attribution 4.0 International (CC BY 4.0)
**File Path**: data/boundaries/eds_national.gpkg.
**ORIGINAL CRS:**  EPSG:2157

* **Coordinate Reference System (CRS)**
We had to ensure that the layers had the same CRS.
Projected CRS: EPSG:2157 (ITM / Irish Transverse Mercator)

## .gitignore
The .gitignore prevents large, temporary, or user-specific files from being uploaded to GitHub, ensuring  the repository remains lightweight, easy to clone, and within GitHub's file size limits.
* **Work Data Folders:** Folders like data/, allowing scripts to process data on your computer without uploading large datasets to GitHub.
* **Python Temporay Files:** it ignores folders like __pycache__/, *.pyc and .ipynb_checkpoints that were generated during code execution.
* **OS System Files:** it blocks operating syatem  metadata files like .DS_Store, Thumbs.db created by macOS and Windows.

## TASKS
* **SPRINT 0: SET-UP AND SPRINT LOG.**
**SETUP**
The team established a free GitHub organization named UCD-GEOG41160-2026-Team-5 with each member designated as an Owner and created a private repository named dublin-extensions-spatial-analysis. We configured the required directory structure (data/, scripts/, and outputs/), initialized README.md, and set up a .gitignore file to exclude large datasets. In sprint 0, the team set up fixed lead roles for each technical task;ExtensionDensity(Q1), GlobalMoran(Q2)and LISA_GiStar(Q3), alongside a rotating Coordinator role shared equally across all four sprints. Project development followed an incremental version control workflow, ensuring that every team member made transparent, individual code and documentation contributions using their own GitHub account

**Script Execution Order**
To reproduce the analysis from a fresh repository clone, the Python scripts were executed in the following order:
*scripts/Q1_ExtensionDensity.py
*scripts/Q2_GlobalMoran.py
*scripts/Q3_LISA_GiStar.py

**SPRINT LOG**
* **ITEM 1: FIRST MEETING  (Setup & Planning)**
  * **DATE OF MEETING:** Friday, 23/10/2026 at 3:00 PM
  * **What Now (Completed & Reviewed):**
    1. Convened team session to thoroughly review the assignment brief.
    2. Agreed on the time duration and milestones for each question.
    3. Assigned fixed lead roles for each technical task (Q1_ExtensionDensity.py, Q2_GlobalMoran.py, Q3_LISA_GiStar.py).
    4. Established the rotating Coordinator role shared equally across all sprints.

  * **What Next: Repository Setup & Task execution of  Sprint 1:**
    1. First team member will create the private GitHub repository and add all teammates as Owners
    2. Team will participate in creating core directory structure (data/, scripts/, outputs/)
    3. First team member will  download raw spatial datasets (planning_applications_national.gpkg, eds_national.gpkg) and start with sprint 1.
    4. Agreed to meet on Thursday at 1:00 PM to review finished tasks.

* **ITEM 2:: Extension density by ED.**
  **Meeting Date:** Thursday, 29/10/2026 at 1:00 PM
  * **What Now (Review of Script:1):**
    1. Convened team session led by the sprint coordinator to review the completed Question 1 workflow (Q1_ExtensionDensity.py).
    2.  The creation of the github, folders and the download of data was done on 27/10/2026.
    3. Executed a test run of the script, identified relative file path issues
    4. Finalized and verified the Question 1 outputs (extensions.duckdb, DublinED_ExtensionDensity.gpkg, and ExtensionDensity_DublinED.png), which were committed to the repository.

  *  **What Next (Sprint 2 Plan:Global Spatial Autocorrelation):**
  * 1. Resolve script issues and recommit to Github
    2. Transitioned to Sprint 2 (Q2_GlobalMoran.py), with work beginning on Friday.
    3. Agreed to reconvene on Monday 2/11/2026 to review the completed Script 2 outputs and spatial autocorrelation results.
    4. Rotate the coordinator for sprint 2

* **ITEM 3: Global Spatial Autocorrelation (Q2_GlobalMoran.py)**
  * **Meeting Date:** Monday, 02/11/2026 at 1:00 PM
  * **What Now (Completed & Reviewed):**
    1. 
    2. 
    3. 

  * **What Next (Sprint 3 :Local Clusters, Hotspots, and Comparison):**
    1. Transitioned to Sprint 3 (Q3_LISA_GiStar.py), with work beginning on Wednesday 4/11/2026.
    2. Agreed to reconvene on Monday, 9/11/2026 at 1:00pm to review the completed Script 3 outputs.
    3. Rotate the Coordinator role for Sprint 3 

* **ITEM 4: Local Clusters, Hotspots, and Comparison (Q3_LISA_GiStar.py)**
  * **Meeting Date:** Monday, 9/11/2026 at 1:00 PM
  * **What Now (Completed & Reviewed):**
    1. 
    2. 
    3. 

  * **What Next (Final Project Review):**
    1. Agreed to reconvene on Wednesday, 11/11/2026 at 1:00 PM to conduct a comprehensive review of all completed scripts, outputs, and documentation across the entire repository.
    
* **ITEM 5: Full Project Review & Repository Verification**
  * **Meeting Date:** Wednesday, 11/11/2026 at 1:00 PM
  * **What Now (Completed & Reviewed):**
    1. Convened as a team to conduct a comprehensive review of all completed scripts (Q1_ExtensionDensity.py, Q2_GlobalMoran.py, and Q3_LISA_GiStar.py) and outputs across the repository.
    2. Identified minor issues in the scripts during end to end testing and assigned follow up fixes to ensure clean execution.

  * **What Next (Final Fixes & Submission):**
    1. Resolve the identified script issues and verify that the entire workflow runs cleanly from start to finish.
    2. Reconvene on Friday, 13/11/2026 to complete the final commit, perform a last quality check on README.md, and generate TeamRepositoryLink.txt for submission.

* **ITEM 6: Final Fixes, Verification & Submission**
    * **Meeting Date:** Friday, 13/11/2026
    * **What Now (Completed & Reviewed):**
      1. Convened for the final team session to verify that all script issues identified on Wednesday were resolved..
      2. Finalized the README.md documentation, verified the repository folder structure (data/, scripts/, outputs/) and commit history across all team members, and pushed the final commits to Github.

  * **What Next (Brightspace Submission):**
    1. Generate and verify TeamRepositoryLink.txt containing the private repository URL and submit it on Brightspace.

* **SPRINT 0: SET-UP**
The team established a free GitHub organization named UCD-GEOG41160-2026-Team-5 with each member designated as an Owner and created a private repository named dublin-extensions-spatial-analysis. We configured the required directory structure (data/, scripts/, and outputs/), initialized README.md, and set up a .gitignore file to exclude large datasets. In sprint 0, the team set up fixed lead roles for each technical task;ExtensionDensity(Q1), GlobalMoran(Q2)and LISA_GiStar(Q3), alongside a rotating Coordinator role shared equally across all four sprints. Project development followed an incremental version control workflow, ensuring that every team member made transparent, individual code and documentation contributions using their own GitHub account

* **SPRINT 1: Extension density by ED.**
In Sprint 1, we set up a DuckDB spatial database (outputs/extensions.duckdb) to filter and process national planning data and Dublin Electoral Divisions, reprojecting layers into Irish Transverse Mercator (EPSG:2157). We then performed spatial joins via SQL to count applications per ED, calculated extension density (applications per_km2), exported the spatial results to DublinED_ExtensionDensity.gpkg, and generated the map visualization ExtensionDensity_DublinED.png

* **SPRINT 2: Global spatial autocorrelation.**
In Sprint 2, we evaluated global spatial autocorrelation for extension density across Dublin Electoral Divisions by testing distribution skewness, applying a log-transformation, and constructing spatial weights matrices. We then computed Global Moran's I with permutation testing for both raw and transformed variables, reporting I and p-values to determine whether the spatial pattern is clustered, dispersed, or random.

* **SPRINT 3 : Local clusters and hotspots.**
In  Sprint 3, we  evaluated local spatial clustering of extension density across Dublin Electoral Divisions using Local Moran's I (LISA) and Getis-Ord Gi, applying false discovery rate (esda.fdr) corrections to control for multiple testing. We generated and exported map visualizations (LISA_ExtensionDensity_DublinED.png, GiStar_ExtensionDensity_DublinED.png) along with a cross-tabulation table (lisa_vs_gistar_crosstab.csv) to compare where and why the two hotspot methods agree or differ

* **SUBMISSION**
After agreeing on the final commit, the team prepared the required deliverables. the shared team files (TeamRepositoryLink.txt, GEOG41160_Assignment2_Team5.zip), were finalized for submission alongside each member's individual PDF reflection submitted to Brightspace.

## VERSION CONTROL
The Git commit history in this repository documnents the iterative development of our project over time.



