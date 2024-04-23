# Inventory of dams in Germany

## Description

Dockerized tool to extract and process data from the the Inventory of dams in Germany for CAMELS-DE.  
A .csv file is saved with information about the dams located in the catchment, the variables listed below. If more than one dam is located inside the catchment boundaries, the information is aggregated for all dams in the catchment. In addition, a .csv file is saved with all non-aggregated / raw data for the dams inside the catchment. Extracted variables are copied to the camelsp `output_data` directory, where other tools process the data further and organize it in the folder structure.

## Container

### Build the container

```bash
docker build -t dams .
```

### Run the container

Follow the instructions in `input_data/README.md` to add the necessary input data to run the tool. 

To run the container, the local `input_data`, `output_data`, `scripts` and `camelsp/output_data` directories have to be mounted inside the container:

```bash
docker run -v ./input_data:/input_data -v ./output_data:/output_data -v ./scripts:/scripts -v /path/to/local/camelsp/output_data:/camelsp/output_data -it --rm dams
```

## Output variables

All variables represent the area percentage of the various HUEK250 classes of the total catchment area.  

- **dams_names** [-] *(names of all dams located in the catchment)* 
- **dams_river_names** [-] *(names of the rivers where the dams are located)*
- **dams_num** [-] *(number of dams located in the catchment)*
- **dams_year_first** [-] *(year when the first dam entered operation)*
- **dams_year_last** [-] *(year when the last dam entered operation)*
- **dams_total_lake_area** [km²] *(total area of all dam lakes at full capacity)*
- **dams_total_lake_volume** [Mio. m³] *(total volume of all dam lakes at full capacity)*
- **dams_purposes** [-] *(purposes of all the dams)* 