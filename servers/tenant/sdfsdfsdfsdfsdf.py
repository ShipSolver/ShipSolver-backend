import requests
import base64

# Read image data
with open("pikachuuuu.jpeg", "rb") as f:
    picturedata = base64.b64encode(f.read()).decode('utf-8')

# Define request payload
payload = {
    "data": {
        "ticketId" : 1,
        "newStatus": "completed_delivery",
        "oldStatus": "in_transit",
        "completingUserId": "0088a8aa-0e5f-4924-a9d5-68ef3cba8cd1",
        "pictures": {
            "POD.jpeg": picturedata,
            "Picture1.jpeg": picturedata,
            "Picture2.jpeg" : picturedata,
            "Picture3.jpeg" : picturedata
        }
    }
}

# Define headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Make POST request
response = requests.post(
    "http://localhost:6767/api/milestones/DeliveryMilestones",
    json=payload,
    headers=headers
)

# Check response
if response.ok:
    print("Request successful")
else:
    print("Request failed with status code", response.status_code)
    print(response.text)
