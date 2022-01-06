CEVA = "CEVA"
NORTH_AMERICAN = "NORTH_AMERICAN"

CEVA_NUM = "1-888-327-8247"


#doclist_keys

HOUSE_REF = "house_ref"
BARCODE = "barcode"
FIRST_PARTY = "first_party"
NUM_PCS = "num_pcs"
PCS = "pcs"
WEIGHT = "weight"

PKG = "pkg"
WT_LBS = "wt(lbs)"
COMMODITY_DESCRIPTION = "commodity_description"
DIMS_IN = "dims(in)"

BOL_NUM = "bol_num"
SPECIAL_SERVICES = "special_services"
SPECIAL_INSTRUCTIONS = "special_instructions"

COMPANY = "company"
NAME = "name"
ADDRESS = "address"
POSTAL_CODE = "postal_code"
PHONE_NUMBER = "phone_number"

CONSIGNEE = "consignee"
SHIPPER = "shipper"

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