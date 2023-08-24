import os
import json
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
openai.api_key = os.environ["OPENAI_API_KEY"]
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer
from google.auth.transport.requests import Request

from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613") # define Large Language Model to be used 
                                                                # and set temp (model's 'creativity') to zero

# access Google Sheet with source websites with Google's OAuth2

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"] # define the scope of access

creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
         flow = InstalledAppFlow.from_client_secrets_file(
             'credentials.json', SCOPES)
         creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
         token.write(creds.to_json())

# Initialize gspread client
client = gspread.authorize(creds)

# Open the sheet
SHEET_ID = '1PiIoCJJW6AVFGATPfqlEG8M8aUPlOCaACOchcGAJNWc'
SHEET_NAME = 'Sheet1'
spreadsheet = client.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)
db = worksheet.get_all_records()
print("Worksheet access successful.")

# Iterate over Forests (areas) and their sources in the Sheet, scraping source by source and storing scraped data in dict (jsons)
forest_count = 0
merged_jsons = {}

for entry in db:
    jsons = {}
    source_count = 0
    for source in entry['Sources'].split(","):
        loader = AsyncChromiumLoader([source])
        html = loader.load() # load source link

        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(html,tags_to_extract=["p", "li", "div", "a", "span"]) # scrape pages with BS

        docs_transformed = docs_transformed[0].page_content[0:] # store entire scraped text as string (sample below)

        # docs_transformed_sample_data = "On March 1, 1872, Yellowstone became the first national park for all to enjoy the unique hydrothermal and geologic features. Within Yellowstone's 2.2 million acres, visitors have unparalleled opportunities to observe wildlife in an intact ecosystem, explore geothermal areas that contain about half the world’s active geysers, and view geologic wonders like the Grand Canyon of the Yellowstone River."

        # Define a schema based on which the LLM will extract data from the scraped text
        # The schema is essentially a prompt and can be defined and redefined based on our needs
        
        from langchain.chains import create_extraction_chain

        schema = {
             "properties": {
                "protected_area_name": {"type": "string"},
                "protected_area_size": {"type": "string"},
                "protected_area_location": {"type": "string"},
                "protected_area_landscape_features": {"type": "string"},
                "protected_area_areas_within": {"type": "string"},
                "protected_area_famous_places_to_visit": {"type": "string"},
                "protected_area_recreational_opportunities": {"type": "string"},
                "protected_area_visitor_infrastructure": {"type": "string"},
                "protected_area_flora": {"type": "string"},
                "protected_area_fauna": {"type": "string"},
                "protected_area_history": {"type": "string"},
                
                },
                "required": ["protected_area_name", "protected_area_size", "protected_area_location"]
            }

        # Extract the data specified in schema
        def extract(content: str, schema: dict):
            return create_extraction_chain(schema=schema, llm=llm).run(content)
            
        protected_area_data = (extract(docs_transformed, schema))

        # Store each result under its source name    
        source_key_name = f"json_{source_count}"
        jsons[source_key_name] = protected_area_data[0]

        source_count += 1

        print("Data extracted!")
        print("Processing data...")

    """ jsons_sample_data = {
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
    
    # Store merged data under the relevant Forest Number
    forest_number = f"forest_{forest_count}"
    if forest_number not in merged_jsons.keys():
        merged_jsons[forest_number] = merged_result
        
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

# Write data forest by forest, adding the forest's official name to col A and dumping all data to col B
for forest_number, data in merged_jsons.items():
    forest_name = data['protected_area_name']
# Convert the dictionary data to a string for writing to the sheet
    data_str = str(data)

    # Append the forest_name and data_str to the sheet
    worksheet.append_row([forest_name, data_str])

    print("Writing successful! Check Google Sheet.")
