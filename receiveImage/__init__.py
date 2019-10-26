import requests
import json
import logging
import azure.functions as func
import datetime
import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess

config = {
    "face-api": {
        "url": "https://hackgt19.cognitiveservices.azure.com/face/v1.0/detect",
        "key": "4e575b9e583d4c2189801f7bc8f86ce6"
    }
}

# Get and check Face API Configuration
face_api = config["face-api"]
face_api_url = face_api['url']
face_api_key = face_api['key']


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    pid = req.params.get("pid")
    

    headers = {'Ocp-Apim-Subscription-Key': face_api_key}
    headers_disk = {
        'Ocp-Apim-Subscription-Key': face_api_key,
        'content-type': 'application/octet-stream'
    }
    params = {
        'returnFaceId':
        'true',
        'returnFaceLandmarks':
        'false',
        'returnFaceAttributes':
        'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    # with open("sadman.png", "rb") as image:
    #  f = image.read()
    #   b = bytearray(f)
    #   var = b[0]
    #   print(b)
    #
    # print(response.json())
    # response = requests.post(face_api_url, params=params,
    #                         headers=headers, json={"url": image_url})

    response = requests.post(face_api_url,
                             params=params,
                             headers=headers_disk,
                             data=req.get_body())

    anger = response.json()[0]['faceAttributes']['emotion']['anger']
    contempt = response.json()[0]['faceAttributes']['emotion']['contempt']
    fear = response.json()[0]['faceAttributes']['emotion']['fear']
    happiness = response.json()[0]['faceAttributes']['emotion']['happiness']
    neutral = response.json()[0]['faceAttributes']['emotion']['neutral']
    sadness = response.json()[0]['faceAttributes']['emotion']['sadness']

    ts = datetime.timestamp()


    def send_image(imgbytes):
        try:
            # Create the BlockBlockService that is used to call the Blob service for the storage account
            block_blob_service = BlockBlobService(account_name='hackgt19',
                                                  account_key='24wGa1RHd0BnemSDBbqRzvvTAB7Qy4IAN28E9de6OLR98wxnFljJXnKaBtzqJd2F53SmtNZP2NnZCPZkeL6wlQ==')

            # Create a container called 'imageblobs'.
            container_name = 'imageblobs'
            block_blob_service.create_container(container_name)
            blob_name = str(pid) + "-" + str(ts)
            # Set the permission so the blobs are public.
            block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)


            # Upload the created file, use local_file_name for the blob name
            block_blob_service.create_blob_from_bytes(container_name, blob_name, imgbytes)
            # List the blobs in the container
            logging.info("\nList blobs in the container")
            generator = block_blob_service.list_blobs(container_name)
            for blob in generator:
                logging.info("\t Blob name: " + blob.name)

        except Exception as e:
            logging.info(e)
    send_image(req.get_body())
    def es(ang, con, fea, hap, neu, sad):
        return hap + .5 * neu - sad - .5 * fea - .5 * con - .5 * ang

    value = es(anger, contempt, fear, happiness, neutral, sadness)
    logging.info("es: " + value)

    params = {
        "ts": ts,
        "value": value,
        "pid": pid,
    }

    logging.info(params)

    res = requests.post("https://swagv1.azurewebsites.net/api/insertEScore",
                        params=params)

    logging.info("Emotional Score: " +
                 str(es(anger, contempt, fear, happiness, neutral, sadness)))
    logging.info(json.dumps(response.json()))

    # need to return es as HTTP response
    return func.HttpResponse(json.dumps({"value": value}), status_code=200)
