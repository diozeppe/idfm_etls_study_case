def transform(payload, staging_table, engine):
    import utils.transformers as tf
    import pandas as pd

    df = pd.DataFrame(payload)

    transformations = {
        "to_normalized_date": [
            "valid_fromdate",
            "valid_todate"
        ],

        "drop": [
            "colourprint_cmjn",
            "textcolourprint_hexa",
            "picto"
        ],

        "rename": {
            "id_line": "id",
            "name_line": "name",
            "shortname_line": "short_name",
            "transportmode": "transport_mode",
            "transportsubmode": "transport_submode",
            "type": "type",
            "operatorref": "operator_ref",
            "operatorname": "operator_name",
            "additionaloperators": "additional_operators_ref",
            "networkname": "network_name",
            "colourweb_hexa": "colour_web_hexa",
            "textcolourweb_hexa": "text_colour_web_hexa",
            "colourprint_cmjn": "colour_print_cmjn",
            "textcolourprint_hexa": "text_colour_print_hexa",
            "accessibility": "accessibility",
            "audiblesigns_available": "audible_signs_available",
            "visualsigns_available": "visual_signs_available",
            "id_groupoflines": "group_of_lines_id",
            "shortname_groupoflines": "short_group_name",
            "notice_title": "notice_title",
            "notice_text": "notice_text",
            "picto": "picto",
            "valid_fromdate": "valid_from_date",
            "valid_todate": "valid_to_date",
            "status": "status",
            "privatecode": "private_code",
            "air_conditioning": "air_conditioning",
        }
    }

    df = (
        df
        .pipe(tf.to_normalized_date, cols=transformations["to_normalized_date"])
        .pipe(tf.drop, cols=transformations["drop"])
        .pipe(tf.rename, cols=transformations["rename"])
    )

    df.to_sql(staging_table, engine, if_exists="replace", index=False)
    
    return df
