#!/usr/bin/env python3
"""
Author : esilberberg
Date   : 2022-02-17
Purpose: Name Standardizer: Correct alternative journal names to their approved names
"""
import argparse
import pandas as pd
import os

# --------------------------------------------------
def get_args():
    """Get csv files from the command line"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('''
        █▄░█ ▄▀█ █▀▄▀█ █▀▀
        █░▀█ █▀█ █░▀░█ ██▄

        █▀ ▀█▀ ▄▀█ █▄░█ █▀▄ ▄▀█ █▀█ █▀▄ █ ▀█ █▀▀ █▀█
        ▄█ ░█░ █▀█ █░▀█ █▄▀ █▀█ █▀▄ █▄▀ █ █▄ ██▄ █▀▄
        corrects journal names
        by eric silberberg, 2022
        '''),
        epilog=('''
                                
                ~*~ 𝙟𝙤𝙞𝙣 𝙩𝙝𝙚 𝙘𝙡𝙪𝙗 𝙖𝙩 𝙚𝙧𝙞𝙘𝙨𝙞𝙡𝙗𝙚𝙧𝙗𝙚𝙧𝙜.𝙘𝙤𝙢 ~*~
. . .
'''))
    
    parser.add_argument('journals',
                        metavar='journals',
                        help='a csv file that contains journal names.')
    
    parser.add_argument('approved_names',
                        metavar='approved_names',
                        help='a csv file that matches alternative journal names with their approved names.')
    
    return parser.parse_args()

# --------------------------------------------------
def correct_journal_name(name, csv):
    """Stadardizes journal names based on csv file input of approved names"""
    df_approved_names = pd.read_csv(csv)
    df_approved_names.dropna(inplace=True)
    correct_names = df_approved_names.set_index('alt_name').to_dict()['approved_name']

    if name in correct_names:
        return correct_names.get(name)
    else:
        return name

# --------------------------------------------------
def correct_plos(name):
    """Stadardizes capitalization of PLOS One journal"""
    plos_variants = ('PloS one', 'PloS ONE', 'PLOS One',
                     'PloS One', 'PLOS ONE', 'PLOSOne', 
                     'plos one', 'PLOSONE', 'plosones', 'PLoS One')

    if name in plos_variants:
        name = 'PLOS One'
        return name
    else:
        return name

# --------------------------------------------------
pd.set_option('mode.chained_assignment', None)

def main():
    """Put a glide in your stride"""
    args = get_args()
    journals_csv = args.journals
    approved_names_csv = args.approved_names

    df = pd.read_csv(journals_csv)

    for i in df.index:
        df['journal'][i] = correct_journal_name(df['journal'][i], approved_names_csv)
        df['journal'][i] = correct_plos(df['journal'][i])

    print(df.head())
    
    filename = os.path.basename(journals_csv)
    basename = filename[:-4]
    outfile_name = f'standardized_{basename}.csv'
    df.to_csv(outfile_name, index=False, encoding='utf-8-sig')
    


# --------------------------------------------------
if __name__ == '__main__':
    main()
