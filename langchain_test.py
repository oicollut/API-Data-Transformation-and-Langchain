import os
import json
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from funcs import initialize_google_sheet, remove_repeating_sentences, merge_source_data
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer
from google.auth.transport.requests import Request
from langchain.chains import create_extraction_chain
import openai
openai.api_key = os.environ["OPENAI_API_KEY"]
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613") # define Large Language Model to be used 
                                                                # and set temp (model's 'creativity') to zero


db = initialize_google_sheet() # access Google Sheet with source websites with Google's OAuth2

# Iterate over Forests (areas) and their sources in the Sheet, scraping source by source and storing scraped data in dict (jsons)
forest_count = 0
merged_jsons = {}

for entry in db:
    jsons = {}
    source_count = 0
    for source in entry['Sources'].split(","):
        print('loading source', source)

        loader = AsyncChromiumLoader([source])
        html = loader.load() # load source link

        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(html,tags_to_extract=["p", "li", "div", "a", "span"]) # scrape pages with BS

        docs_transformed = docs_transformed[0].page_content[0:] # store entire scraped text as string (sample below)
        cleaned_scrapings = remove_repeating_sentences(docs_transformed)[0:7000]

        if html[0].page_content == '':
            print('error loading source')
            continue

        # docs_transformed_sample_data = "On March 1, 1872, Yellowstone became the first national park for all to enjoy the unique hydrothermal and geologic features. Within Yellowstone's 2.2 million acres, visitors have unparalleled opportunities to observe wildlife in an intact ecosystem, explore geothermal areas that contain about half the world’s active geysers, and view geologic wonders like the Grand Canyon of the Yellowstone River."
    
        # Define a schema based on which the LLM will extract data from the scraped text
        # The schema is essentially a prompt and can be defined and redefined based on our needs
        
        schema = {
                    "properties": {
                    "protected_area_name": { "type": "string" },
                    "protected_area_size": { "type": "string" },
                    "protected_area_location": { "type": "string" },
                    "protected_area_landscape_features": { "type": "string" },
                    "protected_area_famous_places_to_visit": { "type": "string" },
                    "protected_area_recreational_opportunities": { "type": "string" },
                    "protected_area_visitor_infrastructure": { "type": "string" },
                    "protected_area_flora": { "type": "string" },
                    "protected_area_fauna": { "type": "string" },
                    "protected_area_history": { "type": "string" },
                    "protected_area_geology": { "type": "string" },
                    "protected_area_address": { "type": "string" },
                    "protected_area_contacts": { "type": "string" },
                    "protected_area_fees": { "type": "string" },
                    "protected_area_camping_rules": { "type": "string" },
                    "protected_area_dog_rules": { "type": "string" },
                    "protected_area_parking": { "type": "string" }
                },
                "required": ["protected_area_name", "protected_area_size", "protected_area_location"]
                }


        def extract(content: str, schema: dict):
            return create_extraction_chain(schema=schema, llm=llm).run(content)
        
        protected_area_data = (extract(cleaned_scrapings, schema))

        if not protected_area_data:
            print(f"Error: protected_area_data is empty for source: {source}")
            continue

        if (isinstance(protected_area_data, list)):
            protected_area_data = protected_area_data[0]
           
        source_key_name = f"json_{source_count}" # Store each result under its source name 
      
        jsons[source_key_name] = protected_area_data

        print(f"Data for forest_{forest_count} from source_{source_count} extracted!")
        print("Processing data...")

        source_count += 1
    """
    jsons_sample_data = {
    'json_0': {'protected_area_name': 'Allegheny National Forest', 'protected_area_size': 'approximately 517,000 acres', 'protected_area_location': 'northwestern Pennsylvania', 'protected_area_landscape_features': 'lakes, rivers, trees, rocks', 'protected_area_famous_places_to_visit': 'Kinzua Skywalk, Longhouse National Scenic Byway, Eldred World War II Museum, Bradford Brew Station, Zippo/Case Museum, Jakes Rocks', 'protected_area_recreational_opportunities': 'snowmobiling, cross-country skiing, biking', 'protected_area_visitor_infrastructure': 'Allegheny National Forest Visitors Bureau', 'protected_area_flora': 'various ecosystems', 'protected_area_fauna': 'wildlife', 'protected_area_history': 'munitions plant during World War II'}, 
    'json_1': {'protected_area_name': 'Allegheny National Forest', 'protected_area_size': '23,100 acres', 'protected_area_location': 'Pennsylvania', 'protected_area_landscape_features': 'Allegheny Reservoir, Allegheny River', 'protected_area_areas_within': 'Hickory Creek Wilderness, Allegheny Islands Wilderness', 'protected_area_famous_places_to_visit': 'Kinzua Dam, Allegheny Reservoir', 'protected_area_recreational_opportunities': 'Hunting, fishing, mountain biking, snowmobiling, water sports', 'protected_area_visitor_infrastructure': 'Campgrounds, trails, canoe and boat launches', 'protected_area_flora': 'Black cherry, maple, other hardwoods', 'protected_area_fauna': 'Not mentioned', 'protected_area_history': 'Exploitation of timber, scientific and sustainable management'}
    }"""
    # Now we have a dict with data for each source for the same forest (see sample above), 
    # we can merge them into a single dictionary, keeping only the unique data
    
    
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

    print(merged_result)
    
    substring_to_clear = ["not mentioned", 'no data', 'None', 'none', '"']
    #clean out empty keys where no data has been collected
    merged_result = {k: v for k, v in merged_result.items() if all(
    all(sub not in x for x in (v if isinstance(v, list) else [v])) for sub in substring_to_clear)}
    print("Filtered dictionary:", merged_result)
    break

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

    print(merged_result)
    
    # Store merged data under the relevant Forest Number
    forest_number = f"forest_{forest_count}"
    if forest_number not in merged_jsons.keys():
        merged_jsons[forest_number] = merge_source_data(jsons)

    forest_count +=1
    print(merged_jsons)

    print("Processing successful. Writing result to Google Sheet...")
# Access the target Sheet to write the gathered data

with open('token.json', 'r') as token_file:
    token_data = json.load(token_file)
credentials = Credentials.from_authorized_user_info(token_data)

# Initialize gspread client
client = gspread.authorize(credentials)

# Open the sheet
SHEET_ID = '1I21v0eu5sAeEb0ZwirantxABsx6E8Cnr2DlZACEkgAY'
SHEET_NAME = 'Sheet1'
spreadsheet = client.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)

# Write data row by row, adding the forest's official name to col A and dumping all data to col B
for forest_number, data in merged_jsons.items():
    if isinstance(data['protected_area_name'], list):
        forest_name = data['protected_area_name'][0]
    else:
        forest_name = data['protected_area_name']
# Convert the dictionary data to a string for writing to the sheet
    data_str = str(data)

    # Append the forest_name and data_str to the sheet
    worksheet.append_row([forest_name, data_str])

    print("Writing successful! Check Google Sheet.")