import logging
import json

import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

table_name = "people"
partition_key = "1"

conn_string = "DefaultEndpointsProtocol=https;AccountName=hackgt19;AccountKey=24wGa1RHd0BnemSDBbqRzvvTAB7Qy4IAN28E9de6OLR98wxnFljJXnKaBtzqJd2F53SmtNZP2NnZCPZkeL6wlQ==;EndpointSuffix=core.windows.net"
table = TableService(connection_string=conn_string)
logging.info(table)
# print(table)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # logging.info(table)

    id = req.params.get('id')
    if not id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            id = req_body.get('id')

    logging.info("id: " + id)

    if id:
        person_entity = table.get_entity(table_name, partition_key, "1")
        logging.info(str(person_entity))

        # return func.HttpResponse(json.dumps(person), status_code=200)
        return func.HttpResponse(json.dumps({
            "name": person_entity['name'],
            "school": person_entity['school'],
        }),
                                 status_code=200)
    else:
        return func.HttpResponse("kys", status_code=400)
