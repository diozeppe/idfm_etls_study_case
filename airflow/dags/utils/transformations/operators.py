def transform(payload, staging_table, engine):
    import utils.transformers as tf
    import pandas as pd

    df = pd.DataFrame(payload)

    transformations = {
        "rename": {
            "operatorref": "id",
            "operatorname": "name",
            "housenumber": "street_number",
            "street": "address",
            "addressline1": "address_additional_info",
            "town": "town",
            "postcode": "post_code",
            "postcodeextension": "post_code_extension",
            "phone": "phone",
            "url": "url",
            "furtherdetails": "addtional_details",
            "contactperson": "contact",
            "logo": "logo",
            "email": "email"
        }
    }
            
    df = (
        df.pipe(tf.rename, cols=transformations["rename"])
    )
    
    df.to_sql(staging_table, engine, if_exists="replace", index=False)

    return df
