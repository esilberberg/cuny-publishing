#!/usr/bin/env python3
"""
Author : esilberberg
Date   : 2022-02-16
Purpose: Get Journals: Parse citations to extract journal names
"""
import argparse
import os
import re
from nltk.tokenize import sent_tokenize
import pandas as pd
from datetime import datetime

# --------------------------------------------------
def get_args():
    """Get citation(s) from command line"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('''
            █▀▀ █▀▀ ▀█▀   ░░█ █▀█ █░█ █▀█ █▄░█ ▄▀█ █░░ █▀
            █▄█ ██▄ ░█░   █▄█ █▄█ █▄█ █▀▄ █░▀█ █▀█ █▄▄ ▄█
            parse citations to extract journal names
            by eric silberberg, 2022
        '''),
        epilog=('''
                                
                ~*~ join the club at ericsilberberg.com ~*~
.
'''))
    
    parser.add_argument('citation',
                        metavar='citation',
                        type=str,
                        help='input citations within a CSV file or a singular citation as text. citations in the CSV file must fall under a column named <citation>')
    
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
    outfile_name = f'journals-output-{dt_string}'

    parser.add_argument('-o',
                        '--outfile',
                        help='enter the name of the output file.',
                        metavar='str',
                        type=str,
                        default=outfile_name)

    return parser.parse_args()

# --------------------------------------------------
def get_journal_mla(citation):
    """Examines citation for compliance with MLA format"""

    # Scans for end of article title: expects double quote followed by white space
    if re.search(r'\"\s', citation):
        journal_name_start = re.search(r'\"\s', citation)
        
        # Marks the start of journal name
        start_index = journal_name_start.span()[0]
        sub_citation = citation[start_index:]

        # Scans for end of journal name: expects a comma
        if re.search(r'\,',  sub_citation):
            journal_name_end = re.search(r'\,',  sub_citation)

            # Marks the end of the journal name
            end_index = journal_name_end.span()[0]
            journal_name = sub_citation[2:end_index]

            return journal_name

# --------------------------------------------------
def get_journal_apa(citation):
    """Examines citation for compliance with APA format"""

    # Scans for year XXXX at start of citation
    if re.search(r"\d\d\d\d", citation):
        year = re.search(r"\d\d\d\d", citation)

        # Ignores all text before the year (authors)
        x = year.span()[1] + 4
        sub_citation = citation[x:]

        # Scans for the end of article name marked by a period
        if re.search(r"\.\s", sub_citation):
            journal_name_start = re.search(r"\.\s", sub_citation)

            # Marks the start of the journal name
            start_index = journal_name_start.span()[0]
            journal_name = sub_citation[start_index:]

            # Scans for end of journal name marked by a comma
            if re.search(r"\,", journal_name):
                journal_name_end = re.search(r"\,", journal_name)
                
                # Marks the end of the journal name
                end_index = journal_name_end.span()[0]
                journal_name = journal_name[2:end_index]

                return journal_name

# --------------------------------------------------
def get_journal_by_match(citation):
    """Examines citation to match a journal name that contains the word 'journal'"""
    
    # Splits up citation on periods into tokens (segments)
    tokens = sent_tokenize(citation)

    for t in tokens:

        # Scans for a token containg the work 'journal'
        if re.search(r"Journal", t):

            # Determines if a comma designates the end of the journal name
            if re.search(r"\,\s\d", t):
                x = re.search(r"\,\s\d", t)
                end_index = x.span()[0]
                journal_name = t[:end_index]
            
            # Determines if a period designates the end of the journal name
            elif re.search(r"\.\s\d", t):
                x = re.search(r"\.\s\d", t)
                end_index = x.span()[0]
                journal_name = t[:end_index]
            
            else:
                journal_name = t[:-1]

            return journal_name

# --------------------------------------------------
def run_strategies(citation):
    """Tests each citation for compliance with functions"""

    strategies = [get_journal_mla, get_journal_apa, get_journal_by_match]
    for strat in strategies:
        output = strat(citation)
        if output:
            return output

# --------------------------------------------------
def main():
    """Put a glide in your stride"""
    args = get_args()
    citation = args.citation
    
    if os.path.isfile(citation):
        df = pd.read_csv(citation)

        journals = []
        for i in df.index:
            name = run_strategies(str(df['citation'][i]))
            journals.append(name)

        df['journal'] = journals
        print(df.head())
            
        if args.outfile:
            basename = args.outfile
            outfile_name = f'{basename}.csv'
            df.to_csv(outfile_name, index=False, encoding='utf-8-sig')

    else:
        name = run_strategies(citation)
        print('============================================================')
        print('CITATION:')
        print(citation)
        print()
        print('JOURNAL NAME:')
        print(name)

# --------------------------------------------------
if __name__ == '__main__':
    main()