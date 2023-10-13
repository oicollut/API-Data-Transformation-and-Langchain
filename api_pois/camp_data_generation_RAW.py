import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
from pois_all_funcs import write_to_google_sheet, get_facilities_and_services_from_campsite_list, get_campsite_attributes, get_rules_and_regs_string, get_segments_from_recgov_decsription, linkcheck, remove_tags
import json
from itertools import islice


with open("api_pois/CAMPGROUNDS.json") as campground_data_file:
    campground_data_dict = json.load(campground_data_file)
    print(f"File opened, dict assembled. Dict is {len(campground_data_dict)} campgrounds long.")
    x = 40
    y = 80
    campground_names = [
    "UPPER BILLY CREEK CG",
    "RANCHERIA"
]

    print(f"Iterating over dict to find target {len(campground_names)} campgrounds.")
    for key, value in campground_data_dict.items():
        camp_name = key
        camp_name_value = value
        campsite_data_situation = camp_name_value[1]
        if camp_name in campground_names:
            if campsite_data_situation == "NO ADDITIONAL CAMPSITE DATA":
                print("Executing scenario where no campsite data is given.")
                description_data = camp_name_value[0]['FacilityDescription']
                print(data)
                
                description_data = camp_name_value[0]['FacilityDescription']
                decsription_segmented_list = get_segments_from_recgov_decsription(description_data)
                main_description = remove_tags(decsription_segmented_list[0])
                natural_features = remove_tags(decsription_segmented_list[1])
                recreation = remove_tags(decsription_segmented_list[2])
                faciities = remove_tags(decsription_segmented_list[3])
                nearby_attractions = remove_tags(decsription_segmented_list[4])
                contact_info = remove_tags(decsription_segmented_list[5])
                rules_and_regs = remove_tags(decsription_segmented_list[6])

                data_dict = {}

                facility = camp_name_value[0]

                data_dict["POI_ID"] = ""
                data_dict["Name"] = facility.get("FacilityName", "")
                data_dict["Accessibility"] = facility.get("FacilityAdaAccess", '') if facility.get("FacilityAdaAccess") else ""
                data_dict["Pets"] = "" #"Enter info if available"
                data_dict["MainDescription"] = main_description + "\n" + recreation + "\n" + nearby_attractions
                data_dict["HowToGetThere"] = facility.get("FacilityDirections", "")
                data_dict["Address"] = "" #"Show directions on Google Maps"
                data_dict["ContactInformation"] = f"Phone: {facility.get('FacilityPhone', '')}" if facility.get("FacilityPhone") else ""
                data_dict["Email"] = f"Email: {facility.get('FacilityEmail', '')}" if facility.get("FacilityEmail") else ""
                data_dict["Resources"] = linkcheck(facility_id) #f"{data_dict['Name'].lower()} Campground | USFS" + '\n' + 
                data_dict["Season"] = ""
                data_dict["RulesAndRegulations"] = get_rules_and_regs_string(id) + "\n" + rules_and_regs
                data_dict["FacilitiesAndServices"] = faciities
                data_dict["Coordinates"] = f"{facility.get('FacilityLongitude', '')}, {facility.get('FacilityLatitude', '')}"
            
                worksheet = write_to_google_sheet(SHEET_ID = '1ekYANpWECKDWGmijUAw59ycT3ni1_P7AmuN9wLy1zmE', SHEET_NAME = 'Campground POIs from Rec.gov transformed')

                data_list = list(data_dict.values())

                worksheet.append_row(data_list)
                print("Writing successful! Check Google Sheet.")
                #FOR CAMPGROUNDS WITH INDIVIDUAL CAMPSITE INFO
            else:
                print("Executing scenario where we have campsite data.")
                description_data = camp_name_value[0]['FacilityDescription']
                decsription_segmented_list = get_segments_from_recgov_decsription(description_data)
                main_description = remove_tags(decsription_segmented_list[0])
                natural_features = remove_tags(decsription_segmented_list[1])
                recreation = remove_tags(decsription_segmented_list[2])
                faciities = remove_tags(decsription_segmented_list[3])
                nearby_attractions = remove_tags(decsription_segmented_list[4])
                contact_info = remove_tags(decsription_segmented_list[5])
                rules_and_regs = remove_tags(decsription_segmented_list[6])
                 
                camp_name_value = value
                campsite_data = camp_name_value[1]
                data = camp_name_value[0]['FacilityDescription']
                print(data)

                data_dict = {}

                facility = camp_name_value[0]


                facilities_string = get_facilities_and_services_from_campsite_list(campsite_data)
                id = campsite_data[0]['CampsiteID']
                facility_id = camp_name_value[0]['FacilityID']

                data_dict["POI_ID"] = ""
                data_dict["Name"] = facility.get("FacilityName", "")
                data_dict["Accessibility"] = facility.get("FacilityAdaAccess", '') if facility.get("FacilityAdaAccess") else ""
                data_dict["Pets"] = "" #"Enter info if available"
                data_dict["Alert"] = ""
                data_dict["MainDescription"] = main_description + "\n" + recreation + "\n" + nearby_attractions                
                data_dict["HowToGetThere"] = facility.get("FacilityDirections", "")
                data_dict["Address"] = "" #"Show directions on Google Maps"
                data_dict["ContactInformation"] = f"Phone: {facility.get('FacilityPhone', '')}" if facility.get("FacilityPhone") else ""
                data_dict["Email"] = f"Email: {facility.get('FacilityEmail', '')}" if facility.get("FacilityEmail") else ""
                data_dict["Resources"] = linkcheck(facility_id) #f"{data_dict['Name'].lower()} Campground | USFS" + '\n' + 
                data_dict["Season"] = ""
                data_dict["RulesAndRegulations"] = get_rules_and_regs_string(id) + "\n" + rules_and_regs
                data_dict["FacilitiesAndServices"] = f"{facilities_string}" + "\n" + faciities
                data_dict["Coordinates"] = f"{facility.get('FacilityLongitude', '')}, {facility.get('FacilityLatitude', '')}"

                worksheet = write_to_google_sheet(SHEET_ID = '1ekYANpWECKDWGmijUAw59ycT3ni1_P7AmuN9wLy1zmE', SHEET_NAME = 'Campground POIs from Rec.gov transformed')

                data_list = list(data_dict.values())

                worksheet.append_row(data_list)
                print("Writing successful! Check Google Sheet.")
        else: print("Looking at next campground..")

"""""
#WRITE CAMPSITE NAMES TO GOOGLE SHEET
import time

# Load your namelist from the JSON file
namelist = []
with open("api_pois/CAMPGROUNDS.json") as campground_data_file:
    campgrund_data_dict = json.load(campground_data_file)
    for key, value in islice(campgrund_data_dict.items(), 1001, 2000):
        camp_name_value = value
        facility = camp_name_value[0]
        namelist.append(camp_name_value[0]["FacilityName"])

# Get your worksheet
worksheet = write_to_google_sheet(SHEET_ID='1ekYANpWECKDWGmijUAw59ycT3ni1_P7AmuN9wLy1zmE', SHEET_NAME='All Rec Gov Camp Names')

# Determine the range to update
start_row = 1001
end_row = start_row + len(namelist) - 1

# Prepare the range and values
range_str = f'A{start_row}:A{end_row}'
values = [[name] for name in namelist]

# Update the worksheet in one go
worksheet.update(range_str, values)

print("Writing successful! Check Google Sheet.")

#WRITE FOREST IDS NEXT TO CAMPSITE LIST IN GOOGLE SHEET


forest_id_list = []
with open("api_pois/CAMPGROUNDS.json") as campground_data_file:
    campgrund_data_dict = json.load(campground_data_file)
    for key, value in islice(campgrund_data_dict.items(), 1001, 2000):
        camp_name_value = value
        facility = camp_name_value[0]
        forest_id_list.append(camp_name_value[0]["ParentRecAreaID"])

# Get your worksheet
worksheet = write_to_google_sheet(SHEET_ID='1ekYANpWECKDWGmijUAw59ycT3ni1_P7AmuN9wLy1zmE', SHEET_NAME='All Rec Gov Camp Names')

# Determine the range to update
start_row = 1006
end_row = start_row + len(forest_id_list) - 1

# Prepare the range and values
range_str = f'B{start_row}:B{end_row}'
values = [[forest_id] for forest_id in forest_id_list]

# Update the worksheet in one go
worksheet.update(range_str, values)

print("Writing successful! Check Google Sheet.")
"""