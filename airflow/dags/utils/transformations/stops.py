def transform(payload, staging_table, engine):
    import utils.transformers as tf
    import pandas as pd
    import geopandas as gpd

    df = pd.DataFrame(payload)

    transformations = {
        "to_normalized_date": [
            "arrcreated",
            "arrchanged"
        ],

        "to_geopoint": [
            "arrgeopoint"
        ],

        "rename": {
            "arrid": "id",
            "arrversion": "version",
            "arrcreated": "created",
            "arrchanged": "changed",
            "arrname": "name",
            "arrtype": "type",
            "arrpubliccode": "publiccode",
            "arrxepsg2154": "xepsg2154",
            "arryepsg2154": "yepsg2154",
            "arrtown": "town",
            "arrpostalregion": "postalregion",
            "arraccessibility": "accessibility",
            "arraudiblesignals": "audiblesignals",
            "arrvisualsigns": "visualsigns",
            "arrfarezone": "farezone",
            "arrgeopoint": "geopoint"
        }
    }

    df = (
        df
        .pipe(tf.to_normalized_date, cols=transformations["to_normalized_date"])
        .pipe(tf.to_geopoint, cols=transformations["to_geopoint"])
        .pipe(tf.rename, cols=transformations["rename"])
    )

    gdf = gpd.GeoDataFrame(df, geometry='geopoint', crs="EPSG:4326")

    gdf.to_postgis(staging_table, engine, if_exists="replace", index=False)
    
    return gdf
