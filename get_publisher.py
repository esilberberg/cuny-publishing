#!/usr/bin/env python3
"""
Author : esilberberg
Date   : 2022-02-25
Purpose: Get Publisher: Look up a journal's publisher through Sherpa Romeo's API
"""
import argparse
import requests
import pandas as pd

# --------------------------------------------------
def get_args():
    """Get csv files from the command line"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('''

        ▒█▀▀█ ▒█▀▀▀ ▀▀█▀▀  ▒█▀▀█ ▒█░▒█ ▒█▀▀█ ▒█░░░ ▀█▀ ▒█▀▀▀█ ▒█░▒█ ▒█▀▀▀ ▒█▀▀█ 
        ▒█░▄▄ ▒█▀▀▀ ░▒█░░  ▒█▄▄█ ▒█░▒█ ▒█▀▀▄ ▒█░░░ ▒█░ ░▀▀▀▄▄ ▒█▀▀█ ▒█▀▀▀ ▒█▄▄▀ 
        ▒█▄▄█ ▒█▄▄▄ ░▒█░░  ▒█░░░ ░▀▄▄▀ ▒█▄▄█ ▒█▄▄█ ▄█▄ ▒█▄▄▄█ ▒█░▒█ ▒█▄▄▄ ▒█░▒█
        retrieve a journal's publisher through SherpaRomeo's API
        by eric silberberg, 2022

n.b. requires an API key from https://v2.sherpa.ac.uk/cgi/register saved to a file <SR-api-key.txt> that lives in the same directory
        '''),
        epilog=('''
                                
                ~*~ join the club at ericsilberberg.com ~*~
.
'''))
    
    parser.add_argument('journals',
                        metavar='journals',
                        help='a csv file that contains journal names in column labeled <journal>')
    
    return parser.parse_args()
# --------------------------------------------------

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

# --------------------------------------------------

def main():
    """Put a glide in your stride"""

    args = get_args()
    journals = args.journals


    df = pd.read_csv(journals)
    df.dropna(inplace=True)

    publishers = []
    for i in df.index:
        try:
            publisher_name = get_publisher(str(df['journal'][i]))
            publishers.append(publisher_name)
            print(i)
            print(df['journal'][i])
            print(publisher_name)
            print('---------------------------')
        except IndexError:
            publishers.append('Error')
            print(i)
            print('Error')
            print('---------------------------')
            
            
    df['publisher'] = publishers
    df.to_csv('get-publisher-results.csv', index=False, encoding='utf-8-sig')
    print(df.head())

# --------------------------------------------------

if __name__ == '__main__':
    main()