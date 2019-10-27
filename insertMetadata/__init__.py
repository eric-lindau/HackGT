import logging
import json
import uuid
from datetime import datetime
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

table_name = "metadata"
partition_key = "1"

conn_string = "DefaultEndpointsProtocol=https;AccountName=hackgt19;AccountKey=24wGa1RHd0BnemSDBbqRzvvTAB7Qy4IAN28E9de6OLR98wxnFljJXnKaBtzqJd2F53SmtNZP2NnZCPZkeL6wlQ==;EndpointSuffix=core.windows.net"
table = TableService(connection_string=conn_string)
logging.info(table)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(str(req.url))
    logging.info(str(req.get_body()))

    now = datetime.now()
    # logging.info(table)
    pid = req.params.get('pid')
    ts = int(now.timestamp() * 100)
    site = req.get_json()['site']

    metadata = Entity()
    metadata.PartitionKey = "1"
    metadata.RowKey = str(uuid.uuid4())
    metadata.pid = pid
    metadata.ts = ts
    metadata.site = site

    etag = table.insert_entity(table_name, metadata)

    return func.HttpResponse(str(metadata.RowKey), status_code=200)