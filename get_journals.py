import re
import pandas as pd

df = pd.read_excel('faculty productivity/sample-citations.xlsx')

def get_journal(citation):

    year = re.search(r"\d\d\d\d", citation)

    x = year.span()[1] + 4
    y = len(citation)

    sub_cite = citation[x:y]

    j_start = re.search(r"\.\s", sub_cite)
    j_end = re.search(r"\,", sub_cite)

    js_index = j_start.span()[0]
    je_index = j_end.span()[1]

    journal = sub_cite[js_index:je_index]

    return journal[2:-1]


journals = []
for i in df.index:
    try:
        journals.append(get_journal(df['citation'][i]))
    except:
        journals.append('error')

df['journal'] = journals

df.to_excel('output.xlsx', index=False)

