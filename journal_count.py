#!/usr/bin/env python3
"""
Author : esilberberg
Date   : 2022-02-25
Purpose: Journal Count: Tallies the number of publications per journal
"""
import argparse
import pandas as pd
import os

# --------------------------------------------------

def get_args():
    """Get a csv file containing citations and journal titles"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('''

                ░░█ █▀█ █░█ █▀█ █▄░█ ▄▀█ █░░   █▀▀ █▀█ █░█ █▄░█ ▀█▀
                █▄█ █▄█ █▄█ █▀▄ █░▀█ █▀█ █▄▄   █▄▄ █▄█ █▄█ █░▀█ ░█░
                tallies the number of publications per journal
                by eric silberberg, 2022
        '''),
        epilog=('''
                                
                ~*~ join the club at ericsilberberg.com ~*~
.
'''))
    parser.add_argument('csv',
                        metavar='csv_file',
                        help='must be a CSV file that includes a column labeled: journal_name')
    
    return parser.parse_args()

# --------------------------------------------------

def strip_hyphens(name):
    """Removes hyphen from journal name"""
    name = str(name).replace('-', ' ')
    return name

# --------------------------------------------------

def main():
    """Put a glide in your stride"""
    args = get_args()
    csv = args.csv
    if os.path.isfile(csv):
        df = pd.read_csv(csv)
        
        # Clean journal names for more accurate tally
        df['journal'] = df['journal'].str.strip()
        df['journal'] = df['journal'].apply(strip_hyphens)
        df['journal'] = df['journal'].str.lower()

        # Time to tally
        df = df['journal'].value_counts().rename_axis(
            'journal').reset_index(name='count')

        # Export
        df.to_csv('journal-count.csv', index=False, encoding='utf-8-sig')
        print(df.head())

    else:
        print('Program requires input in the form of a CSV file.')

# --------------------------------------------------

if __name__ == '__main__':
    main()
