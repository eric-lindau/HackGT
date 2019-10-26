import requests
import json

with open('config.JSON') as config_file:
    data = json.load(config_file)
# set to your own subscription key value
subscription_key = data["subKey"]
assert subscription_key

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
with open("img.png", "rb") as image:
  f = image.read()
  b = bytearray(f)
  #var = b[0]
  #print(b)
response = requests.post(face_api_url, params=params,
                         headers=headers_disk, data=b)
#print(response.json())
#response = requests.post(face_api_url, params=params,
 #                        headers=headers, json={"url": image_url})

hap = response.json()[0]['faceAttributes']['emotion']['happiness']
print(hap)
print(json.dumps(response.json()))