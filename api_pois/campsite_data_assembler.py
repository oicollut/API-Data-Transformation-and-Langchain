import json


campground_dict = {}
all_campground_dicts = {}
with open("/Users/Sasha/Documents/Python_Stuff/Langchain/RIDBFullExport_V1_JSON/Facilities_API_v1.json") as facility_api:
    facility_data_dict = json.load(facility_api)
with open("/Users/Sasha/Documents/Python_Stuff/Langchain/RIDBFullExport_V1_JSON/Campsites_API_v1.json") as campsite_api:
    campsite_data_dict = json.load(campsite_api)

    for facility in facility_data_dict["RECDATA"]:
        if facility["FacilityTypeDescription"] == "Campground":
            key = "FacilityID"
            value = facility[key]
            matching_campsites = [d for d in campsite_data_dict['RECDATA'] if d[key] == value]
            if len(matching_campsites) > 0:
                campground_dict[facility['FacilityName']] = facility, matching_campsites
            else: campground_dict[facility['FacilityName']] = facility, "NO ADDITIONAL CAMPSITE DATA"
            all_campground_dicts.update(campground_dict)
with open("CAMPGROUNDS.json", "w") as outfile:
    json.dump(all_campground_dicts, outfile, indent=4)

