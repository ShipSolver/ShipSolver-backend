# PREREQUISITE THAT SERVER IS RUNNING
import requests

base_url = "localhost:6767"


# res = requests.get("http://127.0.0.1:6767/api/ticket/")

# print(res.text)


# ticket_post = {
#     "ticket": {
#         "BOLNumber": 6969696,
#         "barcodeNumber": 217208336,
#         "claimedNumberOfPieces": 2,
#         "consigneeAddress": "4118FitzgeraldBurgSuite235\\nRaymondport,ND07676",
#         "consigneeCompany": "Patterson,EllisonandRobinson",
#         "consigneeName": "JuliePeck",
#         "consigneePhoneNumber": "(500)641-3584x1623",
#         "consigneePostalCode": "36502",
#         "customerId": 5,
#         "houseReferenceNumber": 132808692,
#         "isPickup": False,
#         "orderS3Link": "s3link",
#         "pieces": "Dayhumannaturalfirmissuethree.",
#         "shipperAddress": "041DiazViaSuite320\\nFloresshire,LA17551",
#         "shipperCompany": "LaraLLC",
#         "shipperName": "DanielleKim",
#         "shipperPhoneNumber": "704.024.9306x13357",
#         "shipperPostalCode": "40684",
#         "specialInstructions": "Strongseekresponsesurfaceoperationstationsimple.",
#         "specialServices": "Stopchoicebooklightbelieve.",
#         "ticketEventId": 4,
#         "ticketId": 4,
#         "timestamp": 1657265927,
#         "userId": 503500753,
#         "weight": 177,
#     }
# }

# res = requests.post("http://127.0.0.1:6767/api/ticket/", json=ticket_post)

# print(res.text)

res = requests.get("http://127.0.0.1:6767/api/ticket/status/ticket_created")

print(res.text)


# http://127.0.0.1:6767/api/ticket/?start=2022-01-01T00:00:00&end=2022-04-04T00:00:00&shipperName=Eric%20Shea
# curl http://127.0.0.1:6767/api/ticket/?shipperName
# # curl http://127.0.0.1:6767/api/ticket?key=a
# # curl http://127.0.0.1:6767/api/ticket/?start=2022-01-01T00:00:00Z&end=2022-04-04T00:00:00Z
