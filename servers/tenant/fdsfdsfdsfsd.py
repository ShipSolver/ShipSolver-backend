import requests
import base64

# Make POST request
response = requests.get("http://localhost:6767/api/milestones/DeliveryMilestones/4")

# Check response
if response.ok:
    print("Request successful")
    print(response.text)
else:
    print("Request failed with status code", response.status_code)
    print(response.text)
