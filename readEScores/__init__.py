import logging
import json

import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

table_name = "escores"
partition_key = "1"

conn_string = "DefaultEndpointsProtocol=https;AccountName=hackgt19;AccountKey=24wGa1RHd0BnemSDBbqRzvvTAB7Qy4IAN28E9de6OLR98wxnFljJXnKaBtzqJd2F53SmtNZP2NnZCPZkeL6wlQ==;EndpointSuffix=core.windows.net"
table = TableService(connection_string=conn_string)
logging.info(table)
# print(table)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # logging.info(table)

    pid = req.params.get("pid")
    logging.info("pid: " + pid)

    if pid:
        pfilter = f"pid eq '{pid}'"

        escore_entities = table.query_entities(table_name, filter=pfilter)

        escores = []

        for entity in escore_entities:
            logging.info(str(entity))
            escore = {
                "value": entity["value"],
                "ts": entity["ts"],
            }
            escores.append(escore)

        headers = {"Access-Control-Allow-Origin": "*"}

        # return func.HttpResponse(json.dumps(person), status_code=200)
        return func.HttpResponse(json.dumps(escores),
                                 status_code=200,
                                 headers=headers)
    else:
        return func.HttpResponse("kys", status_code=400)
