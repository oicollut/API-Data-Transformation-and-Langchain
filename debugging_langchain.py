import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from funcs import initialize_google_sheet, remove_repeating_sentences, merge_source_data
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer
from google.auth.transport.requests import Request
import openai
from langchain.chains import create_extraction_chain
openai.api_key = os.environ["OPENAI_API_KEY"]
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")


loader = AsyncChromiumLoader(["https://en.wikipedia.org/wiki/Park"])
html = loader.load() # load source link
        
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html,tags_to_extract=["p", "li", "div", "a", "span"]) # scrape pages with BS

docs_transformed = docs_transformed[0].page_content[0:] # store entire scraped text as string (sample below)
cleaned_scrapings = remove_repeating_sentences(docs_transformed)
print(cleaned_scrapings)

"""""

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

cleaned_scrapings = "Walk among lush ferns and giant trees\xa0in the magnificence of nature at this 805-acre park that preserves some of California's natural treasures. Beneath the soaring redwood canopy of Sonoma County's Armstrong Redwoods State Natural Reserve, you'll feel silenced by the trees' majesty and humbled by their endurance of more than a thousand years. Whether you're coming to stretch your legs, learn about the history and geology of these splendid trees, or\xa0 take a moment of mindfulness in one of Sonoma County's most"


def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).run(content)

protected_area_data = (extract(cleaned_scrapings, schema))
print(protected_area_data)
"""""



#merged_result = {'protected_area_name': 'Auburn State Recreation Area', 'protected_area_size': ['40 miles', 'over 35,000 acres', '40-miles'], 'protected_area_location': ['gold country', 'Auburn, California', 'heart of “gold country”'], 'protected_area_recreational_opportunities': ['hiking, swimming, boating, fishing, camping, mountain biking, gold panning, horseback riding trails, off-highway motorcycle riding, whitewater recreation', 'hiking, swimming, boating, fishing, camping, mountain biking, gold panning, equestrian/horseback riding trails and off-highway motorcycle riding', 'whitewater rafting, hiking', 'trail running, hiking, swimming, boating, fishing, camping, mountain biking, gold panning, horseback riding, road bicycling, off-highway motorcycle riding, whitewater recreation'], 'protected_area_dog_rules': ['Dogs are welcome on trails, but must be kept on a six-foot leash at all times. Dogs are not allowed on Lake Clementine Road near the dam site, nor in or on Lake Clementine or Upper Lake Clementine.', None, ''], 'protected_area_history': ['Gold Rush Heritage, historic bridges, old railroad routes, Auburn Dam construction site', 'gold miners back in the 1840’s through 1870’s', ''], 'protected_area_contacts': ['(530) 885-4527', 'Phone: 530-885-4527, Reservations: 530-885-4527', None, ''], 'protected_area_fees': ['$10/day use fee/vehicle all areas except Confluence. Camping fees some areas; see web site for details.', '$10 parking fee', ''], 'protected_area_camping_rules': ['Camping is limited to 14 consecutive days, with a 30 day total camping limit per year. Camping is only allowed in designated areas.', None, ''], 'protected_area_address': ['Auburn, California 95603', None, ''], 'protected_area_parking': ['Roadside parking is available.', None, ''], 'protected_area_trails': 'Over 100 miles of hiking and horse trails wind through the steep American River canyons and along the North and Middle Forks of the American River. The most famous trail is the Western States Trail, which runs 100 miles from Lake Tahoe to Auburn, with over 20 miles in the park.', 'protected_area_bicycling_rules': 'Mountain biking and other bicycling is allowed on certain roads and trails in Auburn S. R. A. The maximum speed on all trails is 15 MPH. The maximum speed is 5 MPH when passing pedestrians, equestrians, and when approaching blind curves.', 'protected_area_visitor_infrastructure': ['campgrounds', ''], 'protected_area_flora': [None, ''], 'protected_area_fauna': [None, ''], 'protected_area_geology': ''}
"""
    jsons_sample_data = {
    'json_0': {'protected_area_name': 'Allegheny National Forest', 'protected_area_size': 'approximately 517,000 acres', 'protected_area_location': 'northwestern Pennsylvania', 'protected_area_landscape_features': 'lakes, rivers, trees, rocks', 'protected_area_famous_places_to_visit': 'Kinzua Skywalk, Longhouse National Scenic Byway, Eldred World War II Museum, Bradford Brew Station, Zippo/Case Museum, Jakes Rocks', 'protected_area_recreational_opportunities': 'snowmobiling, cross-country skiing, biking', 'protected_area_visitor_infrastructure': 'Allegheny National Forest Visitors Bureau', 'protected_area_flora': 'various ecosystems', 'protected_area_fauna': 'wildlife', 'protected_area_history': 'munitions plant during World War II'}, 
    'json_1': {'protected_area_name': 'Allegheny National Forest', 'protected_area_size': '23,100 acres', 'protected_area_location': 'Pennsylvania', 'protected_area_landscape_features': 'Allegheny Reservoir, Allegheny River', 'protected_area_areas_within': 'Hickory Creek Wilderness, Allegheny Islands Wilderness', 'protected_area_famous_places_to_visit': 'Kinzua Dam, Allegheny Reservoir', 'protected_area_recreational_opportunities': 'Hunting, fishing, mountain biking, snowmobiling, water sports', 'protected_area_visitor_infrastructure': 'Campgrounds, trails, canoe and boat launches', 'protected_area_flora': 'Black cherry, maple, other hardwoods', 'protected_area_fauna': 'Not mentioned', 'protected_area_history': 'Exploitation of timber, scientific and sustainable management'}
    }

# Initial cleaning: remove None and empty strings from lists
cleaned_dict = {}
for k, v in protected_area_data.items():
    if v is not None:
        if isinstance(v, list):
            cleaned_list = [item for item in v if item is not None and item != '']
            if cleaned_list:  # only add to cleaned_dict if the list is not empty
                cleaned_dict[k] = cleaned_list
        elif v != '':
            cleaned_dict[k] = v

# Remove unwanted substrings


cleaned_dict = {k: v for k, v in cleaned_dict.items() if all(
    all(sub not in x for x in (v if isinstance(v, list) else [v])) for sub in substring_to_clear)}

# Final cleaning: remove empty strings and lists
final_cleaned_dict = {}
for k, v in cleaned_dict.items():
    if isinstance(v, list):
        cleaned_list = [item for item in v if item != '']
        if cleaned_list:
            final_cleaned_dict[k] = cleaned_list
    elif v != '':
        final_cleaned_dict[k] = v

print(final_cleaned_dict)



protected_area_data = {'protected_area_name': 'Armstrong Redwoods State Natural Reserve', 'protected_area_size': '805 acres', 'protected_area_location': 'Sonoma County', 'protected_area_landscape_features': '', 'protected_area_famous_places_to_visit': 'not mentioned', 'protected_area_recreational_opportunities': 'stretch your legs, learn about the history and geology', 'protected_area_visitor_infrastructure': '', 'protected_area_flora': '', 'protected_area_fauna': '', 'protected_area_history': '', 'protected_area_geology': '', 'protected_area_address': '', 'protected_area_contacts': '', 'protected_area_fees': '', 'protected_area_camping_rules': '', 'protected_area_dog_rules': '', 'protected_area_parking': ''}

substring_to_clear = ['not mentioned', 'no data', 'None', 'none', '']

def filter_data(d, substrings_to_exclude):
        
    def is_value_acceptable(value):
        if value is None or value == '':
            return False
        if isinstance(value, list):
            return all(item and item not in substrings_to_exclude for item in value)
        return value not in substrings_to_exclude

    return {k: v for k, v in d.items() if is_value_acceptable(v)}

protected_area_data = filter_data(protected_area_data, substring_to_clear)
print("Filtered dictionary:", protected_area_data)

"""