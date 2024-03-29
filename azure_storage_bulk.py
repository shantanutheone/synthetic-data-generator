from azure.storage.blob import BlobServiceClient, ContentSettings
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os

def write_csv_to_parquet(csv_file, parquet_file):
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Convert DataFrame to Arrow table
    table = pa.Table.from_pandas(df)

    # Write Arrow table to Parquet file
    pq.write_table(table, parquet_file)

def upload_to_azure_storage(parquet_file, sas_connection_string, container_name):
    # Create BlobServiceClient using SAS connection string
    blob_service_client = BlobServiceClient.from_connection_string(sas_connection_string)

    # Get a blob client object
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=parquet_file)

    # Upload Parquet file to Azure Storage
    with open(parquet_file, "rb") as data:
        blob_client.upload_blob(data, overwrite=True, content_settings=ContentSettings(content_type='application/parquet'))

if __name__ == "__main__":
    table_name = "address"
    csv_file = f"database/{table_name}-general.csv"
    parquet_file = f"{table_name}-general.parquet"
    sas_connection_string = os.environ.get("SHARED_SIGNATURE")
    container_name = f"{table_name}-general"

    write_csv_to_parquet(csv_file, parquet_file)

    # Upload Parquet to Azure Storage
    upload_to_azure_storage(parquet_file, sas_connection_string, container_name)

    print("CSV file converted to Parquet and uploaded to Azure Storage successfully.")
