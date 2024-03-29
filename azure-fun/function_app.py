import azure.functions as func
import os
import json
import logging
import json
from openai import OpenAI
import pandas as pd
from generate_data import generate_full_csv
from dotenv import load_dotenv
import os

load_dotenv() 

app = func.FunctionApp()

database_columns = [
        "name-email-general.name",
        "name-email-general.email",
        "address-general.LONGITUDE",
        "address-general.LATITUDE",
        "address-general.STREET",
        "address-general.CITY",
        "address-general.DISTRICT",
        "address-general.REGION",
        "address-general.POSTCODE",
        "mobile-general.mobile",
        "random.random_string"
    ]

sas_token = os.environ.get('AZURE_STORAGE_SAS_TOKEN')

def match_columns(cols) -> dict:
    api_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    
    user_input = json.dumps(cols)
    system_prompt = f"""
    You have database columns - {database_columns}.
    Now User is going to give you the list of columns.
    For each column of user, match it up with exactly 1 nearest matching database column 
    Each value in database columns is of format 'file_name.column_name'.
    Make sure that 
    a. while matching column, ignore file_name and match it with column_name.
    b. while return column, include both ex. 'file_name.column_name'
    Each column from user input should be match to EXACTLY one value of database columns. Don't concatenate multiple matches.
    If match not found, pick "random.random_string"
    Final output should look like this, ex.
    {{
        "longtitude": "address-general.LON",
        "landline": "mobile-general.mobile",
        "cities": "address-general.CITY"
    }}
    """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    response = completion.choices[0].message.content
    return json.loads(response)

@app.route('ai_match_cols', methods=['POST'])
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    columns = req_body.get('columns', [])
    logging.info(f"Columns extracted are, {columns}")
    matched_columns = match_columns(columns)

    generate_full_csv(matched_columns, sas_token)

    df = pd.read_csv('output.csv')
    
    csv_data = df.to_csv(index=False)

    return func.HttpResponse(
        body=csv_data,
        mimetype='text/csv',
        status_code=200
    )