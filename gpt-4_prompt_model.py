import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
from funcs import initialize_google_sheet, write_to_google_sheet

db = initialize_google_sheet(sheet_id='1I21v0eu5sAeEb0ZwirantxABsx6E8Cnr2DlZACEkgAY', sheet_name='Sheet2')

completions_list = []
for entry in db:
    area_data = entry["Data"]
    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "RightOnTrek is a friendly encyclopaedia for hikers in the US."},
        {"role": "user", "content": f"Write a RightOnTrek hiking encyclopaedia article about an area using given data. Text structure: no heading; main description (size, location, geography, landscape and natural features, recreation, infrastructure); Animals and plants section; History and geology section; Other info section (rules, fees, etc.). Character limit 1800 . Data: {area_data}"}
    ]
    )
    print(completion.choices[0].message)
    gpt4_text = completion.choices[0].message
    completions_list.append(gpt4_text)

worksheet = write_to_google_sheet()

next_row = len(worksheet.col_values(3)) + 1

# Append the list of strings row by row to the target column
for i, string in enumerate(completions_list):
    worksheet.update_cell(next_row + i, 3, string)  #
    # Append the forest_name and data_str to the sheet

print("Writing successful! Check Google Sheet.")