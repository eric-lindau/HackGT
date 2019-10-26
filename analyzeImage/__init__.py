import requests
import json
import logging
import azure.functions as func
import datetime

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
                             data=req.body)

    anger = response.json()[0]['faceAttributes']['emotion']['anger']
    contempt = response.json()[0]['faceAttributes']['emotion']['contempt']
    fear = response.json()[0]['faceAttributes']['emotion']['fear']
    happiness = response.json()[0]['faceAttributes']['emotion']['happiness']
    neutral = response.json()[0]['faceAttributes']['emotion']['neutral']
    sadness = response.json()[0]['faceAttributes']['emotion']['sadness']

    def es(ang, con, fea, hap, neu, sad):
        return hap + .5 * neu - sad - .5 * fea - .5 * con - .5 * ang

    value = es(anger, contempt, fear, happiness, neutral, sadness)
    logging.info("es: " + value)
    ts = datetime.timestamp()

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
