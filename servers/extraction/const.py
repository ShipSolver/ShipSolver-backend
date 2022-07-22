CEVA = "CEVA"
NORTH_AMERICAN = "NORTH_AMERICAN"

CEVA_NUM = "1-888-327-8247"


#doclist_keys

BARCODE = "barcodeNumber"
HOUSE_REF = "houseReferenceNumber"
WEIGHT = "weight"
NUM_PCS = "claimedNumberOfPieces"
BOL_NUM = "BOLNumber"
SPECIAL_SERVICES = "specialServices"
SPECIAL_INSTRUCTIONS = "specialInstructions"
CONSIGNEE = "consignee"
SHIPPER = "shipper"
COMPANY = "Company"
NAME = "Name"
ADDRESS = "Address"
POSTAL_CODE = "PostalCode"
PHONE_NUMBER = "PhoneNumber"

NO_SIGNATURE_REQUIRED = "noSignatureRequired"
TAILGATE_AUTHORIZED = "tailgateAuthorized"

FIRST_PARTY = "customerName"

PCS = "pieces"

PKG = "pkg"
WT_LBS = "weight"
COMMODITY_DESCRIPTION = "commodity_description"
DIMS_IN = "dims(in)"


CEVA_SHIPPER_FIELDS = [COMPANY, ADDRESS]
CEVA_CONSIGNEE_FIELDS = [NAME, ADDRESS]

NORTH_AMERICAN_SHIPPER_FIELDS = [COMPANY, NAME, COMPANY, ADDRESS]
NORTH_AMERICAN_CONSIGNEE_FIELDS = [COMPANY, NAME, COMPANY, ADDRESS]
BARCODE_REGEX = "([A-Z][A-Z]\d{3}-\d{7})"
PCS_REGEX = "(\d+) +PCS"
LBS_REGEX = "(\d+) +[Ll]bs"
POSTAL_CODE_REGEX_BOTH = "[ABCEGHJ-NPRSTVXY][\dO][ABCEGHJ-NPRSTV-Z][ -]?[\dO][ABCEGHJ-NPRSTV-Z][\dO]$"
PHONE_NUMBER_REGEX = "((\+\d{1,2}\s)?\(?(905|807|705|647|613|519|416|343|289|226)\)?[\s.-]?\d{3}[\s.-]?\d{4})"

PHONE_COLON_REGEX = "ne: (\d{10})"