#!/bin/bash
# make directories to store the output data if they do not exist
mkdir -p /output_data/scripts

# logging
exec > >(tee -a /output_data/scripts/processing.log) 2>&1

# Start processing
echo "[$(date +%F\ %T)] Starting processing of the Inventory of dams in Germany data for the CAMELS-DE dataset..."

# Download Inventory of dams in Germany data
echo "[$(date +%T)] Downloading Inventory of dams in Germany data..."
python /scripts/00_download_dams_data.py
cp /scripts/00_download_dams_data.py /output_data/scripts/00_download_dams_data.py
echo "[$(date +%T)] Downloaded Inventory of dams in Germany data with 00_download_dams_data.py"

# Extract dam data
echo "[$(date +%T)] Extracting dam data..."
python /scripts/01_process_dams_data.py
cp /scripts/01_process_dams_data.py /output_data/scripts/01_process_dams_data.py
echo "[$(date +%T)] Saved extracted dam data for all CAMELS-DE stations with 01_process_dams_data.py"

# Copy the output data to the camelsp output directory
echo "[$(date +%T)] Copying the extracted and postprocessed data to the camelsp output directory..."
mkdir -p /camelsp/output_data/raw_catchment_attributes/human_influences/dams/
cp -r /output_data/* /camelsp/output_data/raw_catchment_attributes/human_influences/dams/
echo "[$(date +%T)] Copied the extracted and postprocessed data to the camelsp output directory"

# Copy scripts to /camelsp/output_data/scripts/human_influences/dams/
mkdir -p /camelsp/output_data/scripts/human_influences/dams/
cp /output_data/scripts/* /camelsp/output_data/scripts/human_influences/dams/

# Change permissions of the output data
chmod -R 777 /camelsp/output_data/
chmod -R 777 /output_data/
chmod -R 777 /input_data/