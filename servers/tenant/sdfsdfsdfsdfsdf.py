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
    "Accept": "application/json",
    "Authorization": "eyJraWQiOiIxRWhyc0hFbjd5aTFaYklzTGJBeHhCR1I4Ylhjejl0WXF2U3hCUWJpS0xVPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJhMTEyNmVkMS0zOWI4LTQwODUtOTQ1YS00NzIwN2Q2ZTNiNDIiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0yLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMl9Hc05oZ0FaTloiLCJjbGllbnRfaWQiOiI0ZWlxa3VxbGV0djByNWRrdnFkNDNqaDNxYSIsIm9yaWdpbl9qdGkiOiJmMGNmZDcyMC1lOTZkLTQ1NDYtOTMxMC0yMzZjMWNhMDQ3NjQiLCJldmVudF9pZCI6IjMwNWYyN2U3LWYxYWItNDBkOC1iZDAzLTE1YjExZmJhN2U1ZSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2NzgwMzk4MDQsImV4cCI6MTY3ODA0MzQwNCwiaWF0IjoxNjc4MDM5ODA0LCJqdGkiOiJmZjA4MmVlMy0wNTljLTRmMmYtOWQ4Zi1mYmEyZmY3Y2U2YjkiLCJ1c2VybmFtZSI6ImExMTI2ZWQxLTM5YjgtNDA4NS05NDVhLTQ3MjA3ZDZlM2I0MiJ9.wJAxKEsLODWZhnhyGU8801Kh_jPNl7d-S__aWMNopqArwmp-zK2-B9pTvXp_8hNFHBHDSibERLC_NO2EIk9OpsWhBUM9JM5yOd3nSeuR8EPk8n_eK1WWGjxkiCLAl54C0nIvCiDq9TIXodQeqUJX8_DaEiu2tHS4RaC0VPh7Mvk6CWuKVI_Q-cLW-Nn2Ckz1JYP8XCdSQlCtN1uzoS0Bko1vMeOJhqEn6kCi8awgdGCcC8XjCsAy1tA-zYTO0gJKVocQvHabaHtm0DzZlB9A0HohJWIMAz5PieKI1eTcJZhPnJ2m2XyRpJ0BDOPWz68URBtPUehdbWpj51anW3Lrsw"
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
