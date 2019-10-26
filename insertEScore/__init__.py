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
    new_name = req.params.get('name')
    new_school = req.params.get('school')

    new_person = Entity()
    new_person.PartitionKey = "1"
    new_person.RowKey = str(uuid.uuid4())
    new_person.name = new_name
    new_person.school = new_school

    etag = table.insert_entity(table_name, new_person)

    return func.HttpResponse(str(new_person.RowKey), status_code=200)