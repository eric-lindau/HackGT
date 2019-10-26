import logging
import json
import uuid

import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

table_name = "escores"
partition_key = "1"

conn_string = "DefaultEndpointsProtocol=https;AccountName=hackgt19;AccountKey=24wGa1RHd0BnemSDBbqRzvvTAB7Qy4IAN28E9de6OLR98wxnFljJXnKaBtzqJd2F53SmtNZP2NnZCPZkeL6wlQ==;EndpointSuffix=core.windows.net"
table = TableService(connection_string=conn_string)
logging.info(table)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # logging.info(table)
    pid = req.params.get('pid')
    ts = req.params.get('ts')
    value = req.params.get('value')

    components = req.get_json()

    new_es = Entity()
    new_es.PartitionKey = "1"
    new_es.RowKey = str(uuid.uuid4())
    new_es.pid = pid
    new_es.ts = ts
    new_es.value = value
    new_es.components = components

    etag = table.insert_entity(table_name, new_es)

    return func.HttpResponse(str(new_es.RowKey), status_code=200)