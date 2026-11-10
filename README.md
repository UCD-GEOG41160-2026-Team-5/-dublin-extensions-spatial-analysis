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
  * **AGENDA:**
    1. Convened team session to thoroughly review the assignment brief.
    2. Agreed on the time duration and milestones for each question.
    3. Assigned fixed lead roles for each technical task (Q1_ExtensionDensity.py, Q2_GlobalMoran.py, Q3_LISA_GiStar.py).
    * Established the rotating Coordinator role shared equally across all sprints.

  * **NEXT TASKS (Repository Setup & Initialization):**
    1. First team member created the private GitHub repository and added all teammates as Owners
    2. Team participated in creating core directory structure (data/, scripts/, outputs/)
    3. First team member downloaded raw spatial datasets (planning_applications_national.gpkg, eds_national.gpkg)and initiated task execution.
    4. Agreed to meet on Thursday at 1:00 PM to review finished tasks.

* **ITEM 2:**

Sprint 0 0- 27/10/26 at 15:00.
  1. Github created
  2. Folders created
  3. Data downloaded

   **ITEM 1: FIRST MEETING  (Setup & Planning)**
    **ITEM 1: FIRST MEETING  (Setup & Planning)**
     **ITEM 1: FIRST MEETING  (Setup & Planning)**
      **ITEM 1: FIRST MEETING  (Setup & Planning)**
       **ITEM 1: FIRST MEETING  (Setup & Planning)**




Sprint 0 0- 27/10/26 at 15:00.
  1. Github created
  2. Folders created
  3. Data downloaded


* **SPRINT 1: Extension density by ED.**


* **SPRINT 2: Global spatial autocorrelation.**



* **SPRINT 3 : Local clusters and hotspots.**


* **SUBMISSION**
After agreeing on the final commit, the team prepared the required deliverables. the shared team files (TeamRepositoryLink.txt, GEOG41160_Assignment2_Team5.zip), were finalized for submission alongside each member's individual PDF reflection submitted to Brightspace.

## VERSION CONTROL
The Git commit history in this repository documnents the iterative development of our project over time.



  
  2. Folders created
  3. Data downloaded
