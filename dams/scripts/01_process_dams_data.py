from camelsp import get_metadata, Station
import pandas as pd
import geopandas as gpd


def process_dam_data():
    """
    

    """
    # read dam data
    dams_data = gpd.read_file("/input_data/dams/DIG_v1.0.shp")

    # get metadata
    metadata = get_metadata()

    # get list of camels_ids
    camels_ids = metadata["camels_id"].values

    # purposes mapping
    purposes_mapping = {
        "E": "Energy production",
        "HWS": "Flood control",
        "NEG": "Recreational use",
        "TWv": "Water supply",
        "BWv": "Industrial and agricultural water supply",
        "F": "Fishing",
        "NWA": "Transport",
        "NSG": "Nature protection"
    }

    # create empty dataframe to store dam information for each catchment
    df_dams = pd.DataFrame()

    # loop over all camels_ids and fill df_dams with information about dams in the catchment
    for camels_id in camels_ids:
        # initialize Station
        s = Station(camels_id)

        # get catchment
        catchment = s.get_catchment("merit_hydro")

        if catchment is None:
            continue

        # set to crs of dams data
        catchment = catchment.to_crs(dams_data.crs)

        # get dams located in catchment
        dams_in_catchment = gpd.sjoin(dams_data, catchment)[dams_data.columns]

        # set information of dams in catchment in df_dams
        if len(dams_in_catchment) > 0:        
            # dam names
            df_dams.loc[camels_id, "dams_names"] = ", ".join(dams_in_catchment["Name"])

            # dam rivers
            df_dams.loc[camels_id, "dams_river_names"] = ", ".join(dams_in_catchment["river"])

            # number of dams
            df_dams.loc[camels_id, "dams_num"] = int(len(dams_in_catchment))

            # year the first dam entered operation
            if (dams_in_catchment["date_oper"] == -9999.0).any():
                df_dams.loc[camels_id, "dams_year_first"] = pd.NA
            else:
                df_dams.loc[camels_id, "dams_year_first"] = int(dams_in_catchment["date_oper"].min())

            # year the last dam entered operation
            if (dams_in_catchment["date_oper"] == -9999.0).any():
                df_dams.loc[camels_id, "dams_year_last"] = pd.NA
            else:
                df_dams.loc[camels_id, "dams_year_last"] = int(dams_in_catchment["date_oper"].max())

            # total area of all dam lakes
            if (dams_in_catchment["lake_area"] == -9999.0).any():
                df_dams.loc[camels_id, "dams_total_lake_area"] = pd.NA
            else:
                df_dams.loc[camels_id, "dams_total_lake_area"] = round(dams_in_catchment["lake_area"].sum(), 2)

            # total volume of all dam lakes
            if (dams_in_catchment["lake_volum"] == -9999.0).any():
                df_dams.loc[camels_id, "dams_total_lake_volume"] = pd.NA
            else:
                df_dams.loc[camels_id, "dams_total_lake_volume"] = round(dams_in_catchment["lake_volum"].sum(), 2)

            # purposes
            purposes = []
            # get all purposes
            for purpose in dams_in_catchment["purpose"]:
                if purpose is not None:
                    purposes.extend(purpose.split(", "))
            # remove duplicates
            purposes = list(set(purposes))

            purposes_full_names = []

            # map to full names
            for purpose in purposes:
                if purpose not in purposes_mapping:
                    print(f"Unknown purpose: ---{purpose}---")
                    print(purposes)
                else:
                    purposes_full_names.append(purposes_mapping[purpose])
                    
            df_dams.loc[camels_id, "dams_purposes"] = ", ".join(purposes_full_names)
        
        else:
            # set default values if no dams are in the catchment
            df_dams.loc[camels_id, "dams_names"] = ""
            df_dams.loc[camels_id, "dams_river_names"] = ""
            df_dams.loc[camels_id, "dams_num"] = 0
            df_dams.loc[camels_id, "dams_year_first"] = pd.NA
            df_dams.loc[camels_id, "dams_year_last"] = pd.NA
            df_dams.loc[camels_id, "dams_total_lake_area"] = 0
            df_dams.loc[camels_id, "dams_total_lake_volume"] = 0
            df_dams.loc[camels_id, "dams_purposes"] = ""

    # cast correct column types
    df_dams = df_dams.astype({col: "Int64" for col in ["dams_num", "dams_year_first", "dams_year_last"]})
    df_dams = df_dams.astype({col: "float" for col in ["dams_total_lake_area", "dams_total_lake_volume"]})
        
    df_dams.to_csv("/output_data/dams_in_germany.csv", index_label="camels_id")


if __name__ == "__main__":
    process_dam_data()