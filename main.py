import requests
import json

with open('config.JSON') as config_file:
    data = json.load(config_file)
# set to your own subscription key value
subscription_key = data["subKey"]
assert subscription_key
import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )

    # replace <My Endpoint String> with the string from your endpoint URL
    face_api_url = 'https://hackgt19.cognitiveservices.azure.com/face/v1.0/detect'

    image_url = 'https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg'

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    headers_disk = {'Ocp-Apim-Subscription-Key': subscription_key, 'content-type': 'application/octet-stream'}
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }


    #with open("sadman.png", "rb") as image:
     # f = image.read()
      #b = bytearray(f)
      #var = b[0]
      #print(b)

    #print(response.json())
    #response = requests.post(face_api_url, params=params,
     #                        headers=headers, json={"url": image_url})

    response = requests.post(face_api_url, params=params,
                             headers=headers_disk, data=req_body)

    anger = response.json()[0]['faceAttributes']['emotion']['anger']
    contempt = response.json()[0]['faceAttributes']['emotion']['contempt']
    fear = response.json()[0]['faceAttributes']['emotion']['fear']
    happiness = response.json()[0]['faceAttributes']['emotion']['happiness']
    neutral = response.json()[0]['faceAttributes']['emotion']['neutral']
    sadness = response.json()[0]['faceAttributes']['emotion']['sadness']


    def es(ang, con, fea, hap, neu, sad):
        return hap + .5*neu - sad - .5*fea - .5*con - .5*ang

    # need to return es as HTTP response
    return func.HttpResponse(es(anger, contempt, fear, happiness, neutral, sadness), status_code=200)

    print("Emotional Score: " + str(es(anger, contempt, fear, happiness, neutral, sadness)))
    print(json.dumps(response.json()))