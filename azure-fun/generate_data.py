from azure.storage.blob import BlobClient
import pandas as pd
import io
import string
import random


def generate_random_string_df():
    ascii_characters = string.ascii_letters + string.digits 

    random_strings = [''.join(random.choices(ascii_characters, k=8)) for _ in range(200)]

    df = pd.DataFrame({'random_string': random_strings})
    return df

def download_parquet_and_convert_to_df(blob_url, sas_token, limit=200):
    """
    Downloads a Parquet file from Azure Storage using the provided SAS token,
    converts it to CSV, and returns the CSV data as a string.

    Args:
    - blob_url (str): The URL of the Parquet file in Azure Storage.
    - sas_token (str): The SAS token for accessing the Parquet file.

    Returns:
    - str: The CSV data as a string.
    """

    blob_client = BlobClient.from_blob_url(blob_url + '?' + sas_token)

    with io.BytesIO() as stream:
        blob_client.download_blob().readinto(stream)
        stream.seek(0)
        parquet_data = pd.read_parquet(stream)

    parquet_data = parquet_data.head(limit)

    df = pd.DataFrame(parquet_data)
    return df

def generate_single_db_df(database_name, token):
    storage_account = "syntheticdatabase"
    container_name = database_name
    blob_name = database_name
    if(database_name == "random"):
        return generate_random_string_df()
    blob_url = f'https://{storage_account}.blob.core.windows.net/{container_name}/{blob_name}.parquet'
    df_full = download_parquet_and_convert_to_df(blob_url, token)
    return df_full


def generate_full_csv(columns, sas_token):
    headers = [i for i in columns.keys()]
    result_df = pd.DataFrame(columns=headers)

    for csv_head, db, col in [(k, v.split(".")[0], v.split(".")[1]) for k, v in columns.items()]:
        print(csv_head, db, col)
        full_df = generate_single_db_df(db, sas_token)
        result_df[csv_head] = full_df[col]
    result_df.to_csv('output.csv', index=False, header=True)
    




