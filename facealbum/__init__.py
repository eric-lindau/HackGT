import logging
import json
import uuid
import io
import  PIL
from PIL import Image

import cognitive_face as CF
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from azure.storage.blob import BlockBlobService, PublicAccess

table_name = "facebook"
partition_key = "1"

conn_string = "DefaultEndpointsProtocol=https;AccountName=hackgt19;AccountKey=24wGa1RHd0BnemSDBbqRzvvTAB7Qy4IAN28E9de6OLR98wxnFljJXnKaBtzqJd2F53SmtNZP2NnZCPZkeL6wlQ==;EndpointSuffix=core.windows.net"

def getFaceImage(table: TableService, rowkey, rect):
    escores_table = "escores"
    entity = table.get_entity(escores_table, partition_key, rowkey)
    fname = entity.ts

    blob_name = "hackgt19"
    blob_key = "24wGa1RHd0BnemSDBbqRzvvTAB7Qy4IAN28E9de6OLR98wxnFljJXnKaBtzqJd2F53SmtNZP2NnZCPZkeL6wlQ=="
    try:
        container_name = 'imageblobs'
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name=blob_name, account_key=blob_key)

        blob_bytes = block_blob_service.get_blob_to_bytes(container_name, fname)
        logging.info("Downloaded '{}' Successful".format(fname))

        img = Image.open(io.BytesIO(blob_bytes))
        img = img.crop(rect['left'], rect['top'], rect['left'] + rect['width'], rect['top'] + rect['height'])
        
        return img
    except Exception as e:
        logging.error("Error: {}".format(e))

    return None
    

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    CF.BaseUrl.set("https://emotiontrack.cognitiveservices.azure.com/face/v1.0")
    CF.Key.set("4a1e0d41a8494d71ac0b9028464d8e62")
    
    rowkey = req.params.get('rowkey')
    if not rowkey:
        logging.error("Missing parameter(s)")
        return func.HttpResponse("Missing one or more parameter.", status_code=400)
    face = req.get_json()
    face_rect = face['faceRectangle']

    table = TableService(connection_string=conn_string)
    if not table:
        logging.error("Failed to connect to the storage")
        return func.HttpResponse("Failed to connect to the storage. Please try again later.", status_code=500)

    test_img = getFaceImage(table, rowkey, face_rect)
    test_imgIO = io.BytesIO()
    test_img.save(test_imgIO, format='JPG')

    entities = table.query_entities(table_name, filter=None)

    isMatch = False
    for entity in entities:
        img = getFaceImage(table, entity.RowKey, entity.rect)
        imgIO = io.BytesIO()
        img.save(imgIO, format='JPG')

        try:
        res = CF.face.verify(test_imgIO, imgIO)
        if res['isIdentical']:
            # update entry
            entity.RowKey = rowkey
            entity.rect = face_rect
            table.update_entity(table_name, entity)

            isMatch = True
            break

    if not isMatch:
        # new entry
        
        entity = Entity()
        entity.PartitionKey = "1"
        entity.RowKey = str(uuid.uuid4())
        entity.rect = face_rect
        
        table.insert_entity(table_name, entity)

    return func.HttpResponse(entity.RowKey, status_code=200)
