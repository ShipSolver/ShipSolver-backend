import requests
import base64

# Read image data
with open("pikachuuuu.jpeg", "rb") as f:
    picturedata = base64.b64encode(f.read()).decode('utf-8')


# Make POST request
response = requests.get("http://localhost:6767/api/milestones/DeliveryMilestones/1")

# Check response
if response.ok:
    print("Request successful")
    print(response.text)
else:
    print("Request failed with status code", response.status_code)
    print(response.text)
