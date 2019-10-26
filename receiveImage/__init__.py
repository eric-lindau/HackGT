import logging
import azure.functions as func
from azure.storage.blob import BlockBlobService, PublicAccess



def receive_image(ppid, pts):
    try:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name='hackgt19',
                                              account_key='24wGa1RHd0BnemSDBbqRzvvTAB7Qy4IAN28E9de6OLR98wxnFljJXnKaBtzqJd2F53SmtNZP2NnZCPZkeL6wlQ==')
        container_name = 'imageblobs'
        blob_name = str(ppid) + "-" + str(pts)
        bytes = block_blob_service.get_blob_to_bytes(container_name, blob_name)
        return func.HttpResponse(body=bytes, status_code=200, headers={'Content-Type': 'application/octet-stream'})

    except Exception as e:
        logging.info(e)
        return func.HttpResponse(status_code=500)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    pid = req.params.get("pid")
    ts = req.params.get("ts")
    return receive_image(pid, ts)