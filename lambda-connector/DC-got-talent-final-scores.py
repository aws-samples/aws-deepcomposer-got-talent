# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import boto3

def process_data(response):
    data = []
    for row in response['rows']:
        name = row["cells"][0]["formattedValue"]
        score = row["cells"][2]["formattedValue"] ##index [1] retrieves prelim scores, [2] retrieves final scores
        data.append([name,score])
    return data

def lambda_handler(event, context):
    client = boto3.client('honeycode')
    data = []
    
    workbook = "<your wookbook ID>"
    table = "<your table ID>"
    
    response = client.query_table_rows(
        workbookId=workbook,
        tableId=table,
        filterFormula={
            'formula': "=Filter(Composers, \"Composers[Display Final] ORDER BY Composers[Aggregated Final Score] Desc\")"
        }
    )
    
    data += process_data(response)
    
    while("nextToken" in response.keys()):
        print('Next token found in keys!')

        response = client.query_table_rows(
            workbookId=workbook,
            tableId=table,
            filterFormula={
                'formula': "=Filter(Composers, \"Composers[Display Final] ORDER BY Composers[Aggregated Final Score] Desc\")"
            },
            nextToken=response['nextToken']
        )
        data += process_data(response)
    
    return {
        'statusCode': 200,
        "isBase64Encoded": False,
        "headers": {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Credentials': True,
        },
        'body': json.dumps(data)
    }
