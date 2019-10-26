import os, uuid, sys
import io
from datetime import datetime
import azure.functions as func
import requests
import json
import logging
import cognitive_face as CF
from azure.storage.blob import BlockBlobService, PublicAccess


def emotion_score(anger, contempt, fear, happiness, neutral, sadness):
    return happiness + .5 * neutral - sadness - .5 * fear - .5 * contempt - .5 * anger


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Starting Analyze Image Function")

    # Get Configuration
    config = {
        "face-api": {
            "url":
            "https://emotiontrack.cognitiveservices.azure.com/face/v1.0",
            "key": "4e575b9e583d4c2189801f7bc8f86ce6"
        },
        "block-blob": {
            "name":
            "hackgt19",
            "key":
            "24wGa1RHd0BnemSDBbqRzvvTAB7Qy4IAN28E9de6OLR98wxnFljJXnKaBtzqJd2F53SmtNZP2NnZCPZkeL6wlQ=="
        }
    }

    face_api = config["face-api"]
    face_api_url = face_api['url']
    face_api_key = face_api['key']

    block_blob = config["block-blob"]
    block_blob_name = block_blob['name']
    block_blob_key = block_blob['key']

    logging.info("Loaded Face API Configuration")

    CF.BaseUrl.set(face_api_url)
    CF.Key.set(face_api_key)

    # Person ID (Unused)
    pid = req.params.get("pid")

    # headers = {'Ocp-Apim-Subscription-Key': face_api_key}
    # headers_disk = {
    #     'Ocp-Apim-Subscription-Key': face_api_key,
    #     'content-type': 'application/octet-stream'
    # }
    # params = {
    #     'returnFaceId':
    #     'true',
    #     'returnFaceLandmarks':
    #     'false',
    #     'returnFaceAttributes':
    #     'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    # }
    # response = requests.post(face_api_url,
    #                          params=params,
    #                          headers=headers_disk,
    #                          data=req.get_body())

    # with open("sadman.png", "rb") as image:
    #  f = image.read()
    #   b = bytearray(f)
    #   var = b[0]
    #   print(b)
    #
    # print(response.json())
    # response = requests.post(face_api_url, params=params,
    #                         headers=headers, json={"url": image_url})

    body_content = req.get_body()
    image = io.BytesIO(body_content)

    attributes = ('age,gender,headPose,smile,facialHair,glasses,emotion,hair,'
                  'makeup,occlusion,accessories,blur,exposure,noise')

    try:
        res = CF.face.detect(image, True, False, attributes)

        logging.info("Face API (Detection) succeeded")
        logging.info('{} face(s) has been detected.'.format(len(res)))
    except CF.CognitiveFaceException as exp:
        logging.error('Response: {}. {}'.format(exp.code, exp.msg))

    time_now = datetime.now()
    timestamp = datetime.timestamp(time_now)

    for face in res:
        logging.info(json.dumps(face))

        face_id = face['faceId']
        face_attributes = face['faceAttributes']
        face_emotion = face_attributes['emotion']

        anger = face_emotion['anger']
        contempt = face_emotion['contempt']
        fear = face_emotion['fear']
        happiness = face_emotion['happiness']
        neutral = face_emotion['neutral']
        sadness = face_emotion['sadness']

        es_value = emotion_score(anger, contempt, fear, happiness, neutral,
                                 sadness)

        logging.info("Face-ID: {}".format(face_id))
        logging.info("Emotion Score: {}".format(es_value))

        params = {
            "ts": timestamp,
            "value": es_value,
            "pid": pid,
        }

        logging.info(params)

        logging.info("Uploading Face Data to 'insertEScore' Function")
        response = requests.post(
            "https://swagv1.azurewebsites.net/api/insertEScore",
            data=face,
            params=params)
        if response.status_code == 200:
            logging.info("Upload Successful")
        else:
            logging.error("Error: {}".format(response.json()))

    logging.info("Uploading Image to 'imageblobs' Blob")
    try:
        container_name = 'imageblobs'
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name=block_blob_name,
                                              account_key=block_blob_key)

        # Create a container called 'imageblobs'.
        block_blob_service.create_container(container_name)
        blob_name = str(timestamp)
        # Set the permission so the blobs are public.
        # block_blob_service.set_container_acl( container_name, public_access=PublicAccess.Container)

        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_bytes(container_name, blob_name, body_content)
        # List the blobs in the container
        # logging.info("\nList blobs in the container")
        # generator = block_blob_service.list_blobs(container_name)
        # for blob in generator:
        #     logging.info("\t Blob name: " + blob.name)
        logging.info("Upload '{}' Successful".format(blob_name))
    except Exception as e:
        logging.error("Error: {}".format(e))

    logging.info("Finishing Analyze Image Function")

    # need to return es as HTTP response
    return func.HttpResponse("Success", status_code=200)
