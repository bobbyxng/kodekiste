import pypsa 
import pandas as pd
import geopandas as gpd
import os

### MAPPING

def create_busmap(buses, gdf_regions):
    buses_all = pd.DataFrame(
        index = buses.index,
        columns = ["x", "y", "country", "geometry", "nuts_region", "closest_region"]
        )

    buses_all = gpd.GeoDataFrame(buses_all, crs = "EPSG:4326")

    for country in buses["country"].unique():
        print(country)
        buses_subset = buses.loc[buses["country"] == country].copy()

        buses_subset["nuts_region"] = gpd.sjoin(
            buses_subset, 
            gdf_regions.loc[gdf_regions["country_code"] == country], 
            how="left", 
            predicate="within"
            )["region_code"]
        
        # find the closest polygon in gdf_regions to each bus
        buses_subset["closest_region"] = gpd.sjoin_nearest(
            buses_subset.to_crs(epsg=3857),
            gdf_regions.loc[gdf_regions["country_code"] == country].to_crs(epsg=3857),
            how="left",
            )["region_code"]
        buses_subset.to_crs(epsg=4326, inplace=True)

        buses_subset["nuts_region"] = buses_subset["nuts_region"].fillna(buses_subset["closest_region"])
        buses_all.loc[buses_subset.index] = buses_subset

    busmap = buses_all[["nuts_region", "x", "y", "country", "geometry"]].copy()
    busmap.rename(columns = {"nuts_region": "busmap"}, inplace = True)

    return busmap


def create_common_busmap(busmap, common_buses, gdf_regions):
    gdf_busmap = gpd.GeoDataFrame(
        busmap, 
        crs = "EPSG:4326", 
        geometry = "geometry"
        )
    
    gdf_regions_common = gdf_regions.loc[gdf_regions.index.isin(common_buses)]
    regions_to_replace = set(gdf_busmap["busmap"]).difference(set(common_buses))
    buses_to_remap = gdf_busmap["busmap"].isin(regions_to_replace)

    for idx, row in gdf_busmap[buses_to_remap].iterrows():
        country = row["country"]
        gdf_regions_common = gdf_regions[(gdf_regions["country_code"] == country) & gdf_regions.index.isin(common_buses)]

        gdf_busmap.loc[idx, "busmap"] = gpd.sjoin_nearest(
            gdf_busmap.loc[[idx]].to_crs(epsg=3857),
            gdf_regions_common.to_crs(epsg=3857),
            how="left",
            )["region_code"].iloc[0]
        
    return gdf_busmap

nuts = "NUTS2"

if nuts == "NUTS2":
    gdf_regions_nuts = gpd.read_file("geojson/nuts2_regions.geojson")
elif nuts == "NUTS3":
    gdf_regions_nuts = gpd.read_file("geojson/nuts3_regions.geojson")

# if busmap directory does not exist, create it
if not os.path.exists("busmaps/osm"):
    os.makedirs("busmaps/osm")

if not os.path.exists("busmaps/gridkit"):
    os.makedirs("busmaps/gridkit")

n_base_gridkit = pypsa.Network("entsoegridkit/networks/base.nc")
n_base_osm = pypsa.Network("osm-prebuilt/networks/base.nc")

buses_gridkit = gpd.GeoDataFrame(
    n_base_gridkit.buses.copy()[["x", "y", "country"]], 
    geometry=gpd.points_from_xy(n_base_gridkit.buses.x, n_base_gridkit.buses.y),
    crs = "EPSG:4326"
    )

buses_osm = gpd.GeoDataFrame(
    n_base_osm.buses.copy()[["x", "y", "country"]], 
    geometry=gpd.points_from_xy(n_base_osm.buses.x, n_base_osm.buses.y),
    crs = "EPSG:4326"
    )

busmap_gridkit_nuts = create_busmap(buses_gridkit, gdf_regions_nuts)
busmap_osm_nuts = create_busmap(buses_osm, gdf_regions_nuts)
nbuses_gridkit_nuts = len(busmap_gridkit_nuts["busmap"].unique()) 
nbuses_osm_nuts = len(busmap_osm_nuts["busmap"].unique())

# common buses
common_buses_nuts = pd.Series(list(set(busmap_gridkit_nuts["busmap"]).intersection(set(busmap_osm_nuts["busmap"]))))
len(common_buses_nuts)

busmap_gridkit_common_nuts = create_common_busmap(busmap_gridkit_nuts, common_buses_nuts, gdf_regions_nuts)
busmap_osm_common_nuts = create_common_busmap(busmap_osm_nuts, common_buses_nuts, gdf_regions_nuts)
set_diff = set(busmap_osm_common_nuts["busmap"]) - set(busmap_gridkit_common_nuts["busmap"])
print(f"After: {set_diff}")
len(set_diff)

busmap_gridkit_common_nuts[["busmap"]] \
    .to_csv(f"busmaps/gridkit/custom_busmap_elec_s_{len(busmap_gridkit_common_nuts.busmap.unique())}_entsoegridkit.csv")

busmap_osm_common_nuts[["busmap"]] \
    .to_csv(f"busmaps/osm/custom_busmap_elec_s_{len(busmap_osm_common_nuts.busmap.unique())}_osm-prebuilt.csv")