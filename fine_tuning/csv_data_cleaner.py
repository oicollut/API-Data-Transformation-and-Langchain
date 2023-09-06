import pandas as pd
import json

### Delete unneeded metagata fields
# 1. Load the CSV into a Pandas DataFrame.
"""df = pd.read_csv('html_cleaned_csv_file.csv', delimiter=';')


rows_to_chuck = ['foodStorageInfo', 'weatherInfo']

pattern = '|'.join(rows_to_chuck)

# Drop rows where the 'value' column contains any of the substrings
df_filtered = df[~df['name'].str.contains(pattern, case=False, na=False)]

df_filtered.to_csv('l3_cleaned_csv_file.csv', sep = ";", index=False) """""

### Delete links (<.*?>) or &nbsp
"""""
df = pd.read_csv('html_cleaned_csv_file.csv', delimiter=';')

df['value'] = df['value'].str.replace('&nbsp', '', regex=True)

df.to_csv('nbsp_cleaned_csv_file.csv', sep = ";", index=False)"""""

df = pd.read_csv('cleaned_area_metadata.csv', delimiter=';')



counter = 1  # Initialize a counter to keep track of the number of JSON objects

# Open the file in write mode
json_file_path = 'training_data_test.json'
with open(json_file_path, 'w') as f:
    for id, group in df.groupby('id'):
        group.sort_values('value')
        values_list = group['value'].astype(str).tolist()
        values_string = ' '.join(values_list)
        json_data = {
            "messages": [
                {
                    "role": "system",
                    "content": "RightOnTrek is an encyclopedia about hiking in the US."
                },
                {
                    "role": "user",
                    "content": "..."
                },
                {
                    "role": "assistant",
                    "content": values_string
                }
            ]
        }
        # Dump the JSON data as a string and write it to the file followed by a newline
        f.write(json.dumps(json_data))
        f.write('\n')
        
        # Optionally, print or store the counter value to know the number of the JSON object
        print(f"Written JSON object number {counter}")
        counter += 1


