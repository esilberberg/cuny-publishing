import requests
import pandas as pd

# _________________________________________________________________________
def get_publisher(journal):
    """Returns a journal's publisher using Sherpa Romeo's API"""

    # Requires an API key from https://v2.sherpa.ac.uk/cgi/register pasted into a txt file that lives in the same directory.
    with open('SR-api-key.txt') as f:
        api_key = f.read()

    base_url = 'https://v2.sherpa.ac.uk/cgi/retrieve_by_id'
    full_url = base_url + '?item-type=publication&api-key=' + api_key + '&format=Json&identifier=' + journal

    requests.get(full_url)
    response = requests.get(full_url)
    data = response.json()

    publisher = data['items'][0]['publishers'][0]['publisher']['name'][0]['name']

    return publisher
# _________________________________________________________________________

df = pd.read_csv('test-journals.csv')
df.dropna(inplace=True)

publishers = []
for i in df.index:
    try:
        publisher_name = get_publisher(str(df['journal'][i]))
        publishers.append(publisher_name)
    except IndexError:
        publishers.append('Error')
        

df['publisher'] = publishers

df.to_csv('journal-count-with-publishers.csv', index=False, encoding='utf-8-sig')

print(df.head())