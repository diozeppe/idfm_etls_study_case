def transform(payload, staging_table, engine):
    import utils.transformers as tf
    import pandas as pd
    import geopandas as gpd

    df = pd.DataFrame(payload)

    transformations = {
        "to_geopoint": [
            "pointgeo"
        ],

        "rename": {
            "id": "id",
            "route_long_name": "route_long_name",
            "stop_id": "stop_id",
            "stop_name": "stop_name",
            "stop_lon": "stop_lon",
            "stop_lat": "stop_lat",
            "operatorname": "operator_name",
            "shortname": "short_name",
            "mode": "mode",
            "pointgeo": "stop_geopoint",
            "nom_commune": "town",
            "code_insee": "code_insee"
        }
    }

    df = (
        df
        .pipe(tf.to_geopoint, cols=transformations["to_geopoint"])
        .pipe(tf.rename, cols=transformations["rename"])
    )

    gdf = gpd.GeoDataFrame(df, geometry="stop_geopoint", crs="EPSG:4326")

    gdf.to_postgis(staging_table, engine, if_exists="replace", index=False)
    
    return gdf
