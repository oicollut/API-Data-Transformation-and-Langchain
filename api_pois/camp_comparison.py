from pois_all_funcs import initialize_google_sheet
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import gspread



def find_camps(described_camp_names):
    sheet_id= '1ekYANpWECKDWGmijUAw59ycT3ni1_P7AmuN9wLy1zmE'
    sheet_name='Campground POIs from Rec.gov transformed'
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
    sheet = spreadsheet.worksheet(sheet_name)
    #db = sheet.get('A2:A500')
    column_c = sheet.col_values(3)  # 3 represents the third column which is C
    #print(column_c)
    # List of camp names to check against

    matching_names = []
    for cell_value in column_c:
        #print(cell_value)
        for name in described_camp_names:
            #print(name)
            if (cell_value.casefold()[:10] in name.casefold()) and (cell_value not in matching_names):
                print(f"Match Found! {name} in {cell_value}")
                matching_names.append((cell_value))  # Storing the row number and the cell value
    return matching_names


def google_sheet(sheet_id='1gFy0iupBrKkuEXUmeHHbUuO_Y-5CnYRV62Vha6gX8tQ', sheet_name='New Californian POIs'):
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
    #db = worksheet.get_all_records()
    db = worksheet.get('A2:A4500')

    print("Worksheet access successful.")
    return db

read_sheet = google_sheet()
pois = [item[0] for item in read_sheet if isinstance(item, list) and len(item) > 0]
matched_pois = []
for poi in pois:
    if 'campground' in poi.casefold():
        matched_pois.append(poi)
#print("Matched pois - ", matched_pois)

matching_camp_names = find_camps(matched_pois)
print(matching_camp_names)

