import re
from nltk.tokenize import sent_tokenize
import pandas as pd


def get_journal_mla(citation):

    if re.search(r'\"\s', citation):
        journal_title_start = re.search(r'\"\s', citation)
        start_index = journal_title_start.span()[0]

        sub_citation = citation[start_index:]

        if re.search(r'\,',  sub_citation):
            journal_title_end = re.search(r'\,',  sub_citation)

            end_index = journal_title_end.span()[0]

            journal_title = sub_citation[2:end_index]
            return journal_title


def get_journal_apa(citation):

    if re.search(r"\d\d\d\d", citation):
        year = re.search(r"\d\d\d\d", citation)

        x = year.span()[1] + 4
        sub_citation = citation[x:]

        if re.search(r"\.\s", sub_citation):
            journal_title_start = re.search(r"\.\s", sub_citation)

            start_index = journal_title_start.span()[0]
            journal_title = sub_citation[start_index:]

            if re.search(r"\,", journal_title):
                journal_title_end = re.search(r"\,", journal_title)
                end_index = journal_title_end.span()[0]

                journal_title = journal_title[2:end_index]

                return journal_title


def get_journal_by_match(citation):

    tokens = sent_tokenize(citation)

    for t in tokens:
        if re.search(r"Journal", t):
            if re.search(r"\,\s\d", t):
                x = re.search(r"\,\s\d", t)
                end_index = x.span()[0]
                journal_name = t[:end_index]
            elif re.search(r"\.\s\d", t):
                x = re.search(r"\.\s\d", t)
                end_index = x.span()[0]
                journal_name = t[:end_index]
            else:
                journal_name = t[:-1]

            return journal_name


df = pd.read_excel(
    r'C:\Users\erics\Desktop\faculty-productivity-main\peer-reviewed-articles.xlsx')

strategies = [get_journal_mla, get_journal_apa, get_journal_by_match]


def run_strategies(citation):
    for strat in strategies:
        output = strat(citation)
        if output:
            return output


journals = []
for i in df.index:
    name = run_strategies(str(df['citation'][i]))
    journals.append(name)

df['journal'] = journals

df.to_csv('output99.csv', index=False, encoding='utf-8-sig')
