import os
import ocrmypdf
import time
import re
from extraction.const import *
import pdfplumber

def ocr(file_path, save_path):
    ocrmypdf.ocr(file_path, save_path)


def read_pdf(file_name, page_num):
    file_path = os.path.join("../text", file_name.split(".")[0], f"{page_num}.txt")
    with open(file_path, "r") as f:
        return f.read()


def read_pdfplumber(file_name, page_num):
    with pdfplumber.open("../data/NORTH_AMERICAN.pdf") as pdf:
        page = pdf.pages[page_num-1]
        page = page.extract_text()
    return page


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
    Special Instructions
"""
def extract_ceva(page):
    lines = page.splitlines()
    ceva_list = {FIRST_PARTY: CEVA}
    # barcode
    matches = re.findall(BARCODE_REGEX, page)
    if matches:
        insert_in_dict(ceva_list, BARCODE, matches[0])
    # NUM PCS
    matches = re.findall(PCS_REGEX, page)
    if matches:
        insert_in_dict(ceva_list, NUM_PCS, matches[0])
    # weight
    matches = re.findall(LBS_REGEX, page)
    if matches:
        insert_in_dict(ceva_list, WEIGHT, f"{matches[0]} lbs")
    # phone number
    matches = re.findall(PHONE_NUMBER_REGEX, page)
    consignee_phone_number = matches[0][0] if matches else ""

    for line_num, line in enumerate(lines):
        # house ref #
        if "house" in line.lower() or "ref #" in line.lower():
            insert_in_dict(ceva_list, HOUSE_REF, line.split(" ")[-1])
        # shipper
        if line.lower().startswith('shipper') or line.lower().endswith('expéditeur'):
            shipper = extract_info_ceva(lines, line_num)
            insert_in_dict(ceva_list, SHIPPER, shipper)

        #consignee
        if is_consignee(line):
            consignee = extract_info_ceva(lines, line_num, is_shipper=False)
            insert_in_dict(consignee, PHONE_NUMBER, consignee_phone_number)
            insert_in_dict(ceva_list, CONSIGNEE, consignee)
        if "instructions" in line.lower():
            special_instructions = extract_special(lines, line_num, ["reference"])
            insert_in_dict(ceva_list, SPECIAL_INSTRUCTIONS, special_instructions)

    return ceva_list


def is_consignee(line):
    return line.lower().startswith('consignee') or line.lower().endswith('consignataire')


def extract_info_ceva(lines, starting_num, is_shipper=True):

    field_index = 0
    curr_field_entry = ""
    shipper_dict = {}
    FIELDS = CEVA_SHIPPER_FIELDS if is_shipper else CEVA_CONSIGNEE_FIELDS
    for index in range(starting_num+1, len(lines)):
        if not lines[index]:
            continue
        # name or company
        if field_index == 0:
            if starts_with_number(lines[index]):
                field_index += 1
                shipper_dict[FIELDS[field_index-1]] = curr_field_entry.rstrip()
                curr_field_entry = ""
            else:
                curr_field_entry += lines[index] + " "

        if FIELDS[field_index] == ADDRESS:
            curr_field_entry += lines[index] + " "
            if is_consignee(lines[index]) or re.findall(POSTAL_CODE_REGEX_BOTH, lines[index]):
                shipper_dict[ADDRESS] = curr_field_entry.rstrip()
                break

    for field in FIELDS:
        if field not in shipper_dict:
            shipper_dict[field] = ""

    postal_code = extract_postal_code(shipper_dict[ADDRESS])
    insert_in_dict(shipper_dict, POSTAL_CODE, postal_code)

    return shipper_dict


def starts_with_number(line):
    return line.split(" ")[0].isnumeric()


def extract_special(lines, starting_num, keywords):
    entry = ""
    outer_break = False
    for index in range(starting_num+1, len(lines)):
        if not lines[index]:
            continue
        for keyword in keywords:
            if keyword in lines[index].lower():
                outer_break = True
                break
        if outer_break:
            break
        entry += lines[index] + " "

    return entry.rstrip()


"""

North American
    1st party 
    BOL # 
    Consignee information
    # PCS
    DIMS
    Special Services

"""

def extract_north_american(page, page_2):
    lines = page.splitlines()
    north_american_list = {FIRST_PARTY: NORTH_AMERICAN}

    # phone number
    matches = re.findall(PHONE_COLON_REGEX, page)
    shipper_phone_number = matches[0] if matches else ""
    consignee_phone_number = matches[1] if len(matches) > 1 else ""

    for line_num, line in enumerate(lines):
        # ref #
        if "ref#" in line.lower():
            ref_num = line.split(" ")[-1]
            if "ref" not in ref_num.lower():
                insert_in_dict(north_american_list, HOUSE_REF, line.split(":")[-1].strip())
        # BOL #
        if "bol" in line.lower():
            bol_num = line.split(" ")[-1]
            if "bol" not in bol_num.lower():
                insert_in_dict(north_american_list, BOL_NUM, line.split(" ")[-1])
        # shipper
        if "shipper" in line.lower():
            shipper = extract_info_north_american(lines, line_num)
            insert_in_dict(shipper, PHONE_NUMBER, shipper_phone_number)
            insert_in_dict(north_american_list, SHIPPER, shipper)
        # consignee
        if "consignee" in line.lower():
            consignee = extract_info_north_american(lines, line_num, is_shipper=False)
            insert_in_dict(consignee, PHONE_NUMBER, consignee_phone_number)
            insert_in_dict(north_american_list, CONSIGNEE, consignee)
        #special services
        if "services" in line.lower():
            special_services = extract_special(lines, line_num, ["question", "issue", "905-277-2000"])
            insert_in_dict(north_american_list, SPECIAL_SERVICES, special_services)

    lines = page_2.splitlines()
    for line_num, line in enumerate(lines):
        if "pkg" in line.lower() or "wt(lbs)" in line.lower():
            pcs = extract_pcs(lines, line_num)
            insert_in_dict(north_american_list, PCS, pcs)


    return north_american_list


def extract_pcs(lines, starting_num):
    pcs = []
    num_pcs = 0
    weight = 0
    for index in range(starting_num+1, len(lines)):
        if len(lines[index]) < 13:
            _num_pcs, _weight = [float(x) for x in lines[index].split(" ")]
            assert _num_pcs == num_pcs and _weight == weight
            break
        second_space = lines[index].find(" ", lines[index].find(" ") + 1)
        dim_nums = [re.findall("\d+\.\d+", x)[0] for x in lines[index].split(" ")[-3:]]
        pkg, wt = lines[index].split(" ")[:2]
        num_pcs += 1
        weight += float(wt)
        commodity_description = lines[index][second_space:].split(dim_nums[0])[0].lstrip().rstrip()
        dims = ' x '.join(dim_nums)
        pcs.append({PKG: pkg, WT_LBS: wt, COMMODITY_DESCRIPTION: commodity_description, DIMS_IN: dims})

    return pcs

def extract_info_north_american(lines, starting_num, is_shipper=True):
    field_index = 0
    curr_field_entry = ""
    shipper_dict = {}
    FIELDS = NORTH_AMERICAN_SHIPPER_FIELDS if is_shipper else NORTH_AMERICAN_CONSIGNEE_FIELDS
    company = False
    company_1 = ""
    name = ""
    company_2 = ""
    address = ""
    for index in range(starting_num+1, len(lines)):
        if not lines[index]:
            continue
        if field_index == 0:
            if "contact" in lines[index].lower():
                company = True
                name = lines[index].split(": ")[-1]
                company_1 = curr_field_entry.rstrip()
                curr_field_entry = ""
                field_index += 2
                continue
            curr_field_entry += lines[index] + " "
        if company:
            if starts_with_number(lines[index]):
                company = False
                field_index += 1
                company_2 = curr_field_entry.rstrip()
                curr_field_entry = ""
            else:
                curr_field_entry += lines[index] + " "


        if FIELDS[field_index] == ADDRESS:
            curr_field_entry += lines[index] + " "
            if is_consignee(lines[index]) or re.findall(POSTAL_CODE_REGEX_BOTH, lines[index]):
                address = curr_field_entry.rstrip()
                break

    if is_shipper:
        shipper_dict[COMPANY] = company_2
        shipper_dict[ADDRESS] = address
    else:
        shipper_dict[COMPANY] = company_1
        shipper_dict[NAME] = name
        shipper_dict[ADDRESS] = (company_2 + ", " if company_2 else "") + address

    for field in FIELDS:
        if field not in shipper_dict:
            shipper_dict[field] = ""

    postal_code = extract_postal_code(shipper_dict[ADDRESS])
    insert_in_dict(shipper_dict, POSTAL_CODE, postal_code)
    return shipper_dict

def generate_doclist(_list):
    return {
        FIRST_PARTY: _list[FIRST_PARTY] if FIRST_PARTY in _list else "",
        HOUSE_REF: _list[HOUSE_REF] if HOUSE_REF in _list else "",
        BARCODE: _list[BARCODE] if BARCODE in _list else "",
        PCS: _list[PCS] if PCS in _list else [],
        NUM_PCS: _list[NUM_PCS] if NUM_PCS in _list else "",
        WEIGHT: _list[WEIGHT] if WEIGHT in _list else "",
        BOL_NUM: _list[BOL_NUM] if BOL_NUM in _list else "",
        SPECIAL_SERVICES: _list[SPECIAL_SERVICES] if SPECIAL_SERVICES in _list else "",
        SPECIAL_INSTRUCTIONS: _list[SPECIAL_INSTRUCTIONS] if SPECIAL_INSTRUCTIONS in _list else "",
        CONSIGNEE: {
            COMPANY: _list[CONSIGNEE][COMPANY] if CONSIGNEE in _list and COMPANY in _list[CONSIGNEE] else "",
            NAME: _list[CONSIGNEE][NAME] if CONSIGNEE in _list and NAME in _list[CONSIGNEE] else "",
            ADDRESS: _list[CONSIGNEE][ADDRESS] if CONSIGNEE in _list and ADDRESS in _list[CONSIGNEE] else "",
            POSTAL_CODE: _list[CONSIGNEE][POSTAL_CODE] if CONSIGNEE in _list and POSTAL_CODE in _list[CONSIGNEE] else "",
            PHONE_NUMBER: _list[CONSIGNEE][PHONE_NUMBER] if CONSIGNEE in _list and PHONE_NUMBER in _list[CONSIGNEE] else ""
        },
        SHIPPER: {
            COMPANY: _list[SHIPPER][COMPANY] if SHIPPER in _list and COMPANY in _list[SHIPPER] else "",
            NAME: _list[SHIPPER][NAME] if SHIPPER in _list and NAME in _list[SHIPPER] else "",
            ADDRESS: _list[SHIPPER][ADDRESS] if SHIPPER in _list and ADDRESS in _list[SHIPPER] else "",
            POSTAL_CODE: _list[SHIPPER][POSTAL_CODE] if SHIPPER in _list and POSTAL_CODE in _list[SHIPPER] else "",
            PHONE_NUMBER: _list[SHIPPER][PHONE_NUMBER] if SHIPPER in _list and PHONE_NUMBER in _list[SHIPPER] else ""
        }
    }


def extract(page, plumber_page=None):
    second_party = predict_second_party(page)

    if second_party == CEVA:
        return extract_ceva(page)
    elif second_party == NORTH_AMERICAN:
        return extract_north_american(page, plumber_page)

    return {}

def predict_second_party(page):

    if CEVA.lower() in page.lower() or CEVA_NUM in page:
        return CEVA

    return NORTH_AMERICAN


def insert_in_dict(_dict, key, value):
    if not key in _dict:
        _dict[key] = value


def extract_postal_code(address):
    matches = re.findall(f"({POSTAL_CODE_REGEX_BOTH})", address)
    if not matches:
        return ""
    postal_code = matches[0]

    # correct Os to 0s
    for i in [-3, -1, 1]:
        if postal_code[i] == "O":
            postal_code = list(postal_code)
            postal_code[i] = "0"
            postal_code = ''.join(postal_code)
    return postal_code


if __name__ == "__main__":
    start = time.time()
    ceva = read_pdf("CEVA-ocr.pdf", 1)
    ceva_list = extract(ceva)
    ceva_doclist = generate_doclist(ceva_list)
    print(ceva_doclist)

    print()

    north_american_1 = read_pdf("NORTH_AMERICAN.pdf", 1)
    north_american_2 = read_pdfplumber("NORTH_AMERICAN.pdf", 1)
    north_american_list = extract(north_american_1, plumber_page=north_american_2)
    north_american_doclist = generate_doclist(north_american_list)
    print(north_american_doclist)

    print(time.time()-start)
