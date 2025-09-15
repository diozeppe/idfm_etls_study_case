def transform(payload, staging_table, engine):
    import utils.transformers as tf
    import pandas as pd
    from sqlalchemy.dialects.postgresql import ARRAY, TEXT, JSONB

    disruptions_df = pd.DataFrame(payload['disruptions'])

    disruptions_affected_objs = {id: [] for id in disruptions_df["id"].unique()}

    transformations = {
        "to_normalized_date": [
            "lastUpdate"
        ],

        "rename": {
            "applicationPeriods": "application_periods",
            "lastUpdate": "last_update",
            "shortMessage": "short_message",
        }
    }

    for line in payload["lines"]:
        for impactedObject in line["impactedObjects"]:
            for id in impactedObject["disruptionIds"]:
                disruptions_affected_objs[id].append(impactedObject["id"])

    disruptions_df["affected_objects"] = disruptions_df["id"].map(disruptions_affected_objs)

    disruptions_df = (
        disruptions_df
        .pipe(tf.to_normalized_date, cols=transformations["to_normalized_date"])
        .pipe(tf.rename, cols=transformations["rename"])
    )

    disruptions_df.to_sql(
        staging_table,
        engine,
        if_exists="replace",
        index=False,
        dtype={
            "tags": ARRAY(TEXT),
            "application_periods": JSONB,
            "affected_objects": ARRAY(TEXT),
        }
    )

    return disruptions_df
