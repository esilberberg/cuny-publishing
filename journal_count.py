import pandas as pd

csv = 'publications-2020.csv'

df = pd.read_csv(csv)

# --------------------------------------------------


def standardize_plos(name):
    """Stadardizes capitalization of PLOS One journal"""

    plos_variants = ('PloS one', 'PloS ONE', 'PLOS One',
                     'PloS One', 'PLOS ONE', 'PLOSOne', 'plos one')
    if name in plos_variants:
        return 'PLOS One'
    else:
        return name

# --------------------------------------------------


def strip_hyphens(name):
    """Removes hyphen from journal name"""
    name = str(name).replace('-', ' ')
    return name

# --------------------------------------------------


df['journal_name'] = df['journal_name'].str.strip()

df['journal_name'] = df['journal_name'].apply(standardize_plos)

df['journal_name'] = df['journal_name'].apply(strip_hyphens)

df['journal_name'] = df['journal_name'].str.lower()

df = df['journal_name'].value_counts().rename_axis(
    'journal').reset_index(name='counts')

df.to_excel('journal-count.xlsx', index=False, encoding='utf-8-sig')
