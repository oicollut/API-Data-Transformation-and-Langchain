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

def initialize_google_sheet(sheet_id='1ZA9WVAAhHpmf5ikwPv1W3k1CqYNGY_Zatu5MZTrjkcg', sheet_name='Sheet2'):
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

def write_to_google_sheet():
    with open('token.json', 'r') as token_file:
        token_data = json.load(token_file)
    credentials = Credentials.from_authorized_user_info(token_data)

    # Initialize gspread client
    client = gspread.authorize(credentials)

    # Open the sheet
    SHEET_ID = '1I21v0eu5sAeEb0ZwirantxABsx6E8Cnr2DlZACEkgAY'
    SHEET_NAME = 'Sheet4'
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






