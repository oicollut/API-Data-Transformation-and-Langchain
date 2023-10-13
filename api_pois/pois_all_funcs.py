import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import gspread
import regex
import json
from langchain.chains import create_extraction_chain
from langchain.schema.output_parser import OutputParserException
import openai
openai.api_key = os.environ["OPENAI_API_KEY"]
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0, model="gpt-4")
#gpt-3.5-turbo-16k-0613

def initialize_google_sheet(sheet_id='1ZA9WVAAhHpmf5ikwPv1W3k1CqYNGY_Zatu5MZTrjkcg', sheet_name='Sheet1'):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)
    db = worksheet.get_all_records()

    print("Worksheet access successful.")
    return db

def extract(content: str, schema: dict):
            try:
                return create_extraction_chain(schema=schema, llm=llm).run(content)
            except OutputParserException as e:
                print(f"Error occurred while extracting: {e}")
                # handle the exception in any other way you deem necessary
                return None  # or return a default value

def write_to_google_sheet(SHEET_ID = '1I21v0eu5sAeEb0ZwirantxABsx6E8Cnr2DlZACEkgAY', SHEET_NAME = 'Sheet4'):
    with open('token.json', 'r') as token_file:
        token_data = json.load(token_file)
    credentials = Credentials.from_authorized_user_info(token_data)

    # Initialize gspread client
    client = gspread.authorize(credentials)

    # Open the sheet
    spreadsheet = client.open_by_key(SHEET_ID)
    worksheet = spreadsheet.worksheet(SHEET_NAME)
    return worksheet

def remove_repeating_sentences(text):
    # Split the text by period to get sentences
    sentences = regex.split(r'\.\s{1,2}|(?<=[a-zA-Z])\.(?=[a-zA-Z])', text)

# Remove empty strings that may result from the split
    sentences = [x for x in sentences if x]

    #print(sentences)
    
    # Create lists to store unique sentences and long sentences
    unique_sentences = []
    unique_long_sentences = set()
    
    for sentence in sentences:
        # If the sentence is over 100 characters long
        if len(sentence) > 50:
            # Check if this long sentence is unique
            if sentence not in unique_long_sentences:
                # Add the long sentence to the unique set and list
                unique_long_sentences.add(sentence)
                unique_sentences.append(sentence)
        else:
            # If the sentence is not long, add it to the list without checking for uniqueness
            unique_sentences.append(sentence)
                
    # Combine the list back into a single string
    cleaned_text = ". ".join(unique_sentences)
    
    return cleaned_text

def clean_wiki(text):
    cutoff_string = "Main page Contents Current events Random article"
    if cutoff_string in text:
        cutoff_string_location = text.find(cutoff_string)
    text = text[0:cutoff_string_location]
    return text
    

def split_text_into_batches(text, batch_size=5000, delimiter='.'):
    paragraphs = text.split(delimiter)
    batches = []
    current_batch = []
    current_size = 0

    for paragraph in paragraphs:
        paragraph_len = len(paragraph)
        if current_size + paragraph_len > batch_size:
            batches.append(delimiter.join(current_batch))
            current_batch = []
            current_size = 0

        current_batch.append(paragraph)
        current_size += paragraph_len

    if current_batch:  # Don't forget the last batch
        batches.append(delimiter.join(current_batch))

    return batches

def filter_data(d, substrings_to_exclude):
        
    def is_value_acceptable(value):
        if value is None or value == '':
            return False
        if isinstance(value, list):
            return all(item and item not in substrings_to_exclude for item in value)
        return value not in substrings_to_exclude

    return {k: v for k, v in d.items() if is_value_acceptable(v)}


def merge_source_data(jsons):
        merged_result = {}
        # Merge the JSONs
        for json_key, data in jsons.items():
                for key, value in data.items():
                    # If the key exists in the merged result, append the new value (if it's unique)
                    if key in merged_result:
                        if isinstance(merged_result[key], list):
                            if value not in merged_result[key]:
                                merged_result[key].append(value)
                        else:
                            if value != merged_result[key]:
                                merged_result[key] = [merged_result[key], value]
                    # If the key doesn't exist, add it to the merged result
                    else:
                        merged_result[key] = value
        print("Source data merge successful.")
        return merged_result


"""""
def get_facilities_and_services_from_campsite_list(campsite_data):            # Assuming campsite_data is your list of dictionaries
                # Initialize counters
                types_of_campsites = {}
                ada_accessible_count = {}

                # Iterate over the campsite_data to count the number and types of campsites
                for campsite in campsite_data:
                    campsite_type = campsite["CampsiteType"]
                    is_accessible = campsite["CampsiteAccessible"]
                    
                    # Count the types of campsites
                    if campsite_type in types_of_campsites:
                        types_of_campsites[campsite_type] += 1
                    else:
                        types_of_campsites[campsite_type] = 1
                        
                    # Count ADA accessible campsites by type
                    if is_accessible:
                        if campsite_type in ada_accessible_count:
                            ada_accessible_count[campsite_type] += 1
                        else:
                            ada_accessible_count[campsite_type] = 1
                    
                    host_sites = 0
                    for campsite_type in types_of_campsites:
                        if campsite_type == "MANAGEMENT":
                            host_sites +=1

                total_campsites = len(campsite_data) - host_sites

                renamed_types_of_campsites = {}
                for campsite_type, count in types_of_campsites.items():
                    if campsite_type == "STANDARD NONELECTRIC":
                          renamed_types_of_campsites["suitable for both tents and RVs"] = count
                    if campsite_type == "RV NONELECTRIC":
                         renamed_types_of_campsites["for RVs only"] = count
                    if campsite_type == "TENT ONLY NONELECTRIC":
                         renamed_types_of_campsites["for tents only"] = count
                    if campsite_type == "MANAGEMENT":
                        print("Management site removed")
                    else : renamed_types_of_campsites[campsite_type] = count
                    

                # Construct the string
                facilities_string = f"The campground has {total_campsites} campsites, of which"
                type_strings = []
                for campsite_type, count in renamed_types_of_campsites.items():
                    accessible_count = ada_accessible_count.get(campsite_type, 0)
                    if accessible_count > 0:
                        type_string = f"{count} sites are {campsite_type} ({accessible_count} of these are ADA accessible)"
                    else:
                        type_string = f"{count} sites are {campsite_type}"
                    type_strings.append(type_string)
                if len(type_strings) == 1:
                     facilities_string += type_strings[0] + "."
                if len(type_strings) == 2:
                     facilities_string += type_strings[0] + ", " + "and" + type_strings[1] + "."
                if len(type_strings) == 3:  
                    facilities_string += type_strings[0] + ", " + "and" + type_strings[1] + f"Another {type_strings[1]}" + "."
                else: facilities_string += type_strings[0] + " ".join(type_strings) + "."
                print(facilities_string)
                return facilities_string"""

def get_facilities_and_services_from_campsite_list(campsite_data):
    types_of_campsites = {}
    ada_accessible_count = {}
    host_sites = 0

    for campsite in campsite_data:
        #campsite_id = campsite['CampsiteID']
        campsite_type = campsite["CampsiteType"]
        is_accessible = campsite["CampsiteAccessible"]
        
        if campsite_type == "MANAGEMENT":
            host_sites += 1
            continue
        
        if campsite_type in types_of_campsites:
            types_of_campsites[campsite_type] += 1
        else:
            types_of_campsites[campsite_type] = 1
        
        if is_accessible:
            ada_accessible_count[campsite_type] = ada_accessible_count.get(campsite_type, 0) + 1

    total_campsites = len(campsite_data) - host_sites

    renamed_types_of_campsites = {}
    for campsite_type, count in types_of_campsites.items():
        if campsite_type == "STANDARD NONELECTRIC": 
            renamed_types_of_campsites["suitable for both tents and RVs"] = count
        elif campsite_type == "RV NONELECTRIC":
            renamed_types_of_campsites["for RVs only (no hookups)"] = count
        elif campsite_type == "TENT ONLY NONELECTRIC":
            renamed_types_of_campsites["for tents only"] = count
        elif campsite_type == "STANDARD ELECTRIC":
            renamed_types_of_campsites["suitable for tents and RVs (electric hookups provided)"] = count
        elif campsite_type == "WALK TO":
            renamed_types_of_campsites["walk-to"] = count
        elif campsite_type == "EQUESTRIAN NONELECTRIC":
            renamed_types_of_campsites["reserved for camping with horses"] = count
        elif campsite_type == "GROUP TENT ONLY AREA NONELECTRIC":
            renamed_types_of_campsites["classified as a group area, reserved for tents only, without electric hookups"] = count
        elif campsite_type == "GROUP SHELTER NONELECTRIC":
            renamed_types_of_campsites["group shelters"] = count
        elif campsite_type == "GROUP STANDARD NONELECTRIC":
            renamed_types_of_campsites["classified as a group site, suitable for tents and RVs (no electric hookups provided)"] = count
        elif campsite_type == "GROUP STANDARD ELECTRIC":
            renamed_types_of_campsites["tent and RV group site complete with electric hookups"] = count
        elif campsite_type == "GROUP SHELTER ELECTRIC":
            renamed_types_of_campsites["group shelters with electric hookups"] = count
        elif campsite_type == "RV ELECTRIC":
            renamed_types_of_campsites["RV-only, equipped with electric hookups"] = count
        elif campsite_type == "GROUP STANDARD AREA NONELECTRIC":
            renamed_types_of_campsites["of the group area type, suitable for tents and RVs (no electric hookups provided)"] = count
        else: renamed_types_of_campsites[campsite_type] = count


    facilities_string = f"The campground has {total_campsites} campsites, of which"
    type_strings = []
    for campsite_type, count in renamed_types_of_campsites.items():
        accessible_count = ada_accessible_count.get(campsite_type, 0)
        if count == total_campsites:
            facilities_string = f"The campground has {total_campsites} campsites,"
            type_string = f"all of which are {campsite_type}"
        elif count < total_campsites and count == 1:
            type_string = f"{count} site is {campsite_type}"
        elif count > total_campsites:
            type_string = f"{count} sites are {campsite_type}"
        elif accessible_count == 1:
            type_string += "(1 of these sites is ADA accessible)"
        elif accessible_count > 1:
            type_string += f" ({accessible_count} of these are ADA accessible)"
        type_strings.append(type_string)


    #facilities_string += ' ' + ', '.join(type_strings[:-1])
    if len(type_strings) == 1:
        facilities_string += ' ' + type_strings[0]
    elif len(type_strings) > 1:
        facilities_string += ' ' + ', '.join(type_strings[:-1]) + ' and ' + type_strings[-1]
    facilities_string += '.'

    return facilities_string

def get_campsite_attributes():
    with open("api_pois/CampsiteAttributes_API_v1.json") as attributes_data_file:
        attributes_data_dict = json.load(attributes_data_file)
        print(f"File opened, dict assembled. Dict is {len(attributes_data_dict.values())} campsites long.")
    #print(f"Iterating over dict to find target {len(campsite_IDs)} campgrounds.")
        for key, value in attributes_data_dict.items():
            recdata = key
            campsite_dict_list = value
            all_campground_dicts = {}
            for campsite_dict in campsite_dict_list:
                data_dict = {}
                if "EntityID" in campsite_dict.values():
                    data_dict["CampsiteID"] = campsite_dict["AttributeValue"]
                if "Capacity/Size Rating" in campsite_dict.values():
                    data_dict["CampsiteSize"] = campsite_dict["AttributeValue"]
                if "Checkin Time" in campsite_dict.values():
                    data_dict["CheckIn"] = campsite_dict["AttributeValue"]
                if "Checkout Time" in campsite_dict.values():
                    data_dict["CheckOut"] = campsite_dict["AttributeValue"]
                if "Max Num of People" in campsite_dict.values():
                    data_dict["MaxPeople"] = campsite_dict["AttributeValue"]
                if "Max Num of Vehicles" in campsite_dict.values():
                    data_dict["MaxVehicles"] = campsite_dict["AttributeValue"]
                if "Proximity to Water" in campsite_dict.values():
                    data_dict["Waterfront"] = campsite_dict["AttributeValue"]
                if "Campfire Allowed" in campsite_dict.values():
                    data_dict["CampfireAllowed"] = campsite_dict["AttributeValue"]
                all_campground_dicts.update(data_dict)
    return all_campground_dicts
 

def get_rules_and_regs_string(id):
    with open("/Users/Sasha/Documents/Python_Stuff/Langchain/MY_CAMPSITE_ATTRIBUES.json") as attributes_data_file:
        data_dict = json.load(attributes_data_file)
        if data_dict.get(id):
            check_in = data_dict[id].get('CheckIn', '')
            check_out = data_dict[id].get('CheckOut', '')

            people_rules = []
            vehicle_rules = []

            campsite_size = data_dict[id].get('CampsiteSize', '')
            max_people = data_dict[id].get('MaxPeople', '')
            max_vehicles = data_dict[id].get('MaxVehicles', '')
            
            people_rules.append(f"{max_people} for {campsite_size} campsites")
            vehicle_rules.append(f"{max_vehicles} per {campsite_size} campsite")
                
            people_string = " and ".join(people_rules)
            vehicle_string = " and ".join(vehicle_rules)

            rules_string = f"Check-in time is {check_in}, check-out is at {check_out}. The maximum number of people is {people_string}. The maximum number of vehicles is {vehicle_string}."
        else: rules_string = f"No campsite with id {id} in Campsite Attributes file." 
    print(rules_string)
    return rules_string
    #return data_dict

def remove_tags(text):
    import re
    pattern = r'<[^>]+>'

    clean_text = re.sub(pattern, '', text)

    return clean_text

"""attributes_data_dict = {"RECDATA":[
    {"AttributeID":9,"AttributeName":"Campfire Allowed","AttributeValue":"Yes","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":10,"AttributeName":"Capacity/Size Rating","AttributeValue":"Single","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":11,"AttributeName":"Checkin Time","AttributeValue":"12:00 PM","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":12,"AttributeName":"Checkout Time","AttributeValue":"12:00 PM","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":23,"AttributeName":"Driveway Entry","AttributeValue":"Parallel","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":24,"AttributeName":"Driveway Grade","AttributeValue":"Slight","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":25,"AttributeName":"Driveway Length","AttributeValue":"","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":26,"AttributeName":"Driveway Surface","AttributeValue":"Gravel","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":52,"AttributeName":"Max Num of People","AttributeValue":"6","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":53,"AttributeName":"Max Num of Vehicles","AttributeValue":"2","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":54,"AttributeName":"Max Vehicle Length","AttributeValue":"27","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":65,"AttributeName":"Pets Allowed","AttributeValue":"Yes","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":72,"AttributeName":"Proximity to Water","AttributeValue":"Riverfront","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":314,"AttributeName":"Placed on Map","AttributeValue":"1","EntityID":"1","EntityType":"Campsite"},
    {"AttributeID":10429,"AttributeName":"IS EQUIPMENT MANDATORY","AttributeValue":"true","EntityID":"1","EntityType":"Campsite"}
    ]
}"""


import json

def get_campsite_attributes_json():
    with open("api_pois/CampsiteAttributes_API_v1.json") as attributes_data_file:
        attributes_data_dict = json.load(attributes_data_file)
        print(f"File opened, dict assembled. Dict is {len(attributes_data_dict['RECDATA'])} campsites long.")
    
    all_campground_dicts = {}
    
    for campsite_dict in attributes_data_dict['RECDATA']:
        entity_id = campsite_dict.get("EntityID")
        attribute_name = campsite_dict.get("AttributeName")
        attribute_value = campsite_dict.get("AttributeValue")
        
        if entity_id not in all_campground_dicts:
            all_campground_dicts[entity_id] = {}
            
        if attribute_name == "Capacity/Size Rating":
            all_campground_dicts[entity_id]["CampsiteSize"] = attribute_value
        elif attribute_name == "Checkin Time":
            all_campground_dicts[entity_id]["CheckIn"] = attribute_value
        elif attribute_name == "Checkout Time":
            all_campground_dicts[entity_id]["CheckOut"] = attribute_value
        elif attribute_name == "Max Num of People":
            all_campground_dicts[entity_id]["MaxPeople"] = attribute_value
        elif attribute_name == "Max Num of Vehicles":
            all_campground_dicts[entity_id]["MaxVehicles"] = attribute_value
        elif attribute_name == "Proximity to Water":
            all_campground_dicts[entity_id]["Waterfront"] = attribute_value
        elif attribute_name == "Campfire Allowed":
            all_campground_dicts[entity_id]["CampfireAllowed"] = attribute_value
    
    return all_campground_dicts


def get_segments_from_recgov_decsription(description):
    import re

    matches = re.findall(r'<h2>(.*?)</h2>(.*?)<h2>', description, re.DOTALL)

    sections = {match[0]: match[1].strip() for match in matches}

    # As the last <h2> tag doesn't have a following <h2> to terminate it, it's not in the matches.
    # To get it, we can do another regular expression search:
    last_h2 = re.search(r'<h2>([^<]+)</h2>(.*)', description.split("<h2>")[-1], re.DOTALL)

    if last_h2:
        sections[last_h2.group(1)] = last_h2.group(2).strip()

    # Now, based on your headers, you can assign the values:
    main_description = sections.get('Overview', '')
    recreation = sections.get('Recreation', '')
    facilities = sections.get('Facilities', '')
    natural_features = sections.get('Natural Features', '')
    nearby_attractions = sections.get('Nearby Attractions', '')
    contact_info = sections.get('contact_info', '')
    rules_and_regs = sections.get('Charges &amp; Cancellations', '')

    string_list = []
    string_list.append(main_description)
    string_list.append(natural_features)
    string_list.append(recreation)
    string_list.append(facilities)
    string_list.append(nearby_attractions)
    string_list.append(contact_info)
    string_list.append(rules_and_regs)

    print("Main Description:\n", main_description)
    print("\nRecreation:\n", recreation)
    print("\nFacilities:\n", facilities)
    print("\nNatural Features:\n", natural_features)
    print("\nNearby Attractions:\n", nearby_attractions)
    print("\nContact Info:\n", contact_info)
    print("\nRules and Regulations:\n", rules_and_regs)

        
    return(string_list)

def linkcheck(camp_id):
    import requests
    link1 = f"https://www.recreation.gov/camping/campgrounds/{camp_id}"
    link2 = f"https://www.recreation.gov/camping/campgrounds/{camp_id}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Check if the link works
    response = requests.get(link1, headers=headers)
    if response.status_code == 200 and "Please Bear With Us" not in response.text:
        message = f'Reservations can be made online at <a href="{link1}">Recreation.gov</a> or by calling 1-877-444-6777.'
    else:
        response = requests.get(link2, headers=headers)
        if response.status_code == 200 and "Please Bear With Us" not in response.text:
            message = f'More information is available at <a href="{link2}">Recreation.gov</a>.'
        else: message = "Reservations can be made online at Recreation.gov or by calling 1-877-444-6777."


    return message
