TerraFringe Analytics 

A High-Fidelity Data & Spatial Analytics Dashboard Simulating 30 Years of Ecological Degradation (1996–2026)

TerraFringe Analytics is a comprehensive business intelligence and spatial data science project built in Power BI and Python. It models the cascading effects of habitat fragmentation, hydrological collapse, and human-wildlife conflict across three vital Indian wildlife corridors: Kanha-Pench, Rajaji-Corbett, and Wayanad-Bandipur.

Dashboard Previews

Page 1: Canopy Fragmentation & Spatial Bleed


Visualizing the 30-year inward retreat of the forest canopy using custom Python-generated spatial coordinates mapped in ArcGIS.

Page 2: Socio-Ecological Interface


Tracking the anthropogenic friction—fringe population pressure, waterhole desiccation, and human-wildlife conflict escalation.

 Project Scope & Objectives

The primary objective of TerraFringe Analytics is to bridge the gap between abstract climate metrics and tangible geographic reality. Rather than just showing static numbers, this project:

Spatially Reconstructs forest loss by simulating organic "edge-effect" degradation.

Analyzes Hydrological Collapse by correlating rising land surface temperatures with dropping groundwater tables and streamflow.

Quantifies Socio-Ecological Friction by mapping the direct relationship between shrinking wildlife habitats and escalating human-wildlife conflict in fringe communities.

The Spatial Engine: "Inward-Bleeding" Algorithm

To accurately map canopy loss over time without relying on heavy historical satellite raster processing, this project employs a custom geospatial data pipeline written in Python (GeoPandas, Shapely, NumPy).

Instead of generating a random scatter plot, the script (generate_hotspots.py) simulates natural habitat encroachment:

Distance-Based Sorting: The algorithm generates a 2.2x excess pool of randomized coordinates within the polygon bounds. It measures each point's exact distance from the outer boundary and sorts them so points closest to the edge are selected first.

Organic Fuzziness: A random multiplier (0.7 to 1.3) is applied to the distance sorting, ensuring the shrinking border looks like a jagged, natural bleed rather than perfect geometric rings.

Density Modification: To prevent visual clutter and render engine lag, a scaling factor is applied (e.g., 1 dot = 2 SqKm), preserving mathematical accuracy while keeping the map legible.

Timeline Slicing: The master path of coordinates is sliced dynamically and assigned to a Dim_Epoch timeline (1996–2026) for seamless chronological mapping in Power BI.

 Data Architecture & Modeling

The project utilizes a robust star-schema data model tailored for complex environmental telemetry:

Dim_Epoch: The central timeline governing all historical slices (5-year intervals).

localized_deforestation_events: The generated coordinate dataset mapping specific canopy loss locations over time.

fact_watershed_aquifer_hydrology: Tracks mean perennial streamflow, groundwater table depth, and temperature anomalies.

fact_human_wildlife_conflict & fact_fringe_population: Quantifies the human element, measuring demographic pressure against conflict incidents.

Note: The model includes rigorous data-type enforcement to resolve DAX cyclic reference loops caused by mixed-type financial/scientific metrics.

Dashboard Architecture

Page 1: The Spatial Layer

ArcGIS Timeline Map: Displays the inward-bleeding canopy coordinates, dynamically reacting to the Dim_Epoch slicer.

Key Performance Indicators (KPIs): Tracks Cumulative Canopy Loss (SqKm), Canopy Retained (SqKm), and Average Waterhole Dryout Rate.

Page 2: The Consequence Layer

Conflict Escalation Matrix: Dual-axis charts comparing the rise in Human-Wildlife Conflict incidents against cumulative canopy loss.

Demographic Squeeze: Stacked area charts visualizing the explosive population growth in the fringe zones surrounding the protected corridors.

Hydrological Stress Tracker: Correlates surface temperature spikes with the collapse of local groundwater resources.

Tech Stack

Data Visualization & Modeling: Microsoft Power BI, DAX, Power Query.

Spatial Generation & Processing: Python (Pandas, GeoPandas, Shapely, NumPy).

Mapping Engine: ArcGIS for Power BI.

How to Run the Spatial Generator

If you wish to update the spatial coordinates based on new loss data:

Ensure your Python environment has the required libraries: pip install pandas geopandas shapely numpy

Place yearly_loss_numbers.csv and raw_corridors.geojson in the working directory.

Run the engine: python generate_hotspots.py

Open the Power BI file and click Refresh to load the newly generated localized_deforestation_events.csv.