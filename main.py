import requests
import json
import logging
import azure.functions as func
import cognitive_face as CF

# Setup Logging
logger = logging.getLogger('emotiontrack')
logger.setLevel(logging.DEBUG)

# Setup Console Logging
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Logging Format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add Handler
logger.addHandler(ch)

# Load Config file
with open("config.json") as fp:
    config = json.load(fp)

# Get and check Face API Configuration
face_api = config["face-api"]
assert face_api
face_api_url = face_api['url']
face_api_key = face_api['key']
assert face_api_url
assert face_api_key

CF.BaseUrl.set(face_api_url)
CF.Key.set(face_api_key)

path = "/home/kp/Documents/GitHub/HackGT/eric.jpg"

attributes = (
    'age,gender,headPose,smile,facialHair,glasses,emotion,hair,'
    'makeup,occlusion,accessories,blur,exposure,noise')

try:
    res = CF.face.detect(path, False, False, attributes)

    log_text = 'Response: Success. Detected {} face(s) in {}'.format(
        len(res), path)
    print(res)
    logger.info(log_text)
    text = '{} face(s) has been detected.'.format(len(res))
    logger.info(text)
except CF.CognitiveFaceException as exp:
    logger.error('Response: {}. {}'.format(exp.code, exp.msg))


# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')
#
#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')
#
#     if name:
#         return func.HttpResponse(f"Hello {name}!")
#     else:
#         return func.HttpResponse(
#              "Please pass a name on the query string or in the request body",
#              status_code=400
#         )
#
#     headers = {'Ocp-Apim-Subscription-Key': face_api_key}
#     headers_disk = {'Ocp-Apim-Subscription-Key': face_api_key, 'content-type': 'application/octet-stream'}
#     params = {
#         'returnFaceId': 'true',
#         'returnFaceLandmarks': 'false',
#         'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
#     }
#
#
#     # with open("sadman.png", "rb") as image:
#     #  f = image.read()
#     #   b = bytearray(f)
#     #   var = b[0]
#     #   print(b)
#     #
#     # print(response.json())
#     # response = requests.post(face_api_url, params=params,
#     #                         headers=headers, json={"url": image_url})
#
#     response = requests.post(face_api_url, params=params, headers=headers_disk, data=req_body)
#
#     anger = response.json()[0]['faceAttributes']['emotion']['anger']
#     contempt = response.json()[0]['faceAttributes']['emotion']['contempt']
#     fear = response.json()[0]['faceAttributes']['emotion']['fear']
#     happiness = response.json()[0]['faceAttributes']['emotion']['happiness']
#     neutral = response.json()[0]['faceAttributes']['emotion']['neutral']
#     sadness = response.json()[0]['faceAttributes']['emotion']['sadness']
#
#     def es(ang, con, fea, hap, neu, sad):
#         return hap + .5*neu - sad - .5*fea - .5*con - .5*ang
#
#     # need to return es as HTTP response
#     return func.HttpResponse(es(anger, contempt, fear, happiness, neutral, sadness), status_code=200)
#
#     print("Emotional Score: " + str(es(anger, contempt, fear, happiness, neutral, sadness)))
#     print(json.dumps(response.json()))
