import pdftotext
import os
import ocrmypdf
import time

from const import *

def ocr(file_path, save_path):
    ocrmypdf.ocr(file_path, save_path)


def read_pdf(file_name):
    file_path = os.path.join("data", file_name)
    with open(file_path, "rb") as f:
        return list(pdftotext.PDF(f))


"""
CEVA
    1st party
    Consignee info
        Name
        Addr
        Postal Code
        Phone Number
    House/ref
    Barcode
    Lbs
    # PCs
    Shipper
"""
def extract_ceva(page):
    lines = page.splitlines()
    ceva_list = {}
    for line in lines:
        if "house" or "ref #" in line.lower():
            insert_in_dict(ceva_list, HOUSE_REF, line.split(" ")[-1])




    return ceva_list

"""

North American
    1st party (Amazon etc)
    BOL # 
    Consignee information
    # PCS
    DIMS
    Special Services
    
"""
def extract_north_american(page):

    return {}


def generate_doclist(_list):
    return {
        "first_party": _list["first_party"] if "first_party" in _list else "",
        HOUSE_REF: _list[HOUSE_REF] if HOUSE_REF in _list else "",
        "barcode": _list["barcode"] if "barcode" in _list else "",
        "num_pcs": _list["num_pcs"] if "num_pcs" in _list else "",
        "weight": _list["weight"] if "weight" in _list else "",
        "consignee": {
            "name": _list["consignee"]["name"] if "consignee" in _list and "name" in _list["consignee"] else "",
            "addr": _list["consignee"]["addr"] if "consignee" in _list and "addr" in _list["consignee"] else "",
            "postal_code": _list["consignee"]["postal_code"] if "consignee" in _list and "postal_code" in _list["consignee"] else "",
            "phone_number": _list["consignee"]["phone_numnber"] if "consignee" in _list and "phone_number" in _list["consignee"] else ""
        },
        "shipper": {
            "company": _list["shipper"]["company"] if "shipper" in _list and "company" in _list["shipper"] else "",
            "name": _list["shipper"]["name"] if "shipper" in _list and "name" in _list["shipper"] else "",
            "addr": _list["shipper"]["addr"] if "shipper" in _list and "addr" in _list["shipper"] else "",
            "postal_code": _list["shipper"]["postal_code"] if "shipper" in _list and "postal_code" in _list["shipper"] else "",
            "phone_number": _list["shipper"]["phone_numnber"] if "shipper" in _list and "phone_number" in _list["shipper"] else ""
        },
        "bol_num": _list["bol_num"] if "bol_num" in _list else "",
        "dims": _list["dims"] if "dims" in _list else "",
        "special_services": _list["special_services"] if "special_services" in _list else []
    }


def extract(page):
    second_party = predict_second_party(page)

    if second_party == CEVA:
        return extract_ceva(page)
    elif second_party == NORTH_AMERICAN:
        return extract_north_american(page)

    return {}

def predict_second_party(page):

    if CEVA.lower() in page.lower() or CEVA_NUM in page:
        return CEVA

    return NORTH_AMERICAN


def insert_in_dict(_dict, key, value):
    if not key in _dict:
        _dict[key] = value


if __name__ == "__main__":
    start = time.time()

    # ocr("data/CEVA.pdf", "data/CEVA-ocr.pdf")
    ceva = read_pdf("CEVA-ocr.pdf")
    ceva_list = extract(ceva[0])
    ceva_doclist = generate_doclist(ceva_list)
    print(ceva_doclist)
    north_american = read_pdf("NORTH_AMERICAN.pdf")
    north_american_list = extract(ceva[0])
    north_american_doclist = generate_doclist(ceva_list)
    print(north_american_doclist)

    print(time.time()-start)
