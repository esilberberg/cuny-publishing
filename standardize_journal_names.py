import pandas as pd

csv = 'alt_journal_names.csv'

df_alt_journal_names = pd.read_csv(csv)
df_alt_journal_names.dropna(inplace=True)

titles = ('ACS Pharmacol. Transl. Sci.', 'Commun. Biol.', 'J. Mem. Biol.', 'J. Phys. Chem. A', 'Magic Journal')
	
corrected_journal_names = df_alt_journal_names.set_index('alt_name').to_dict()['full_name']

def correct_journal_name(journal_name):
        if journal_name in corrected_journal_names:
            return corrected_journal_names.get(journal_name)
        else:
            return journal_name

def standardize_plos(name):
    """Stadardizes capitalization of PLOS One journal"""

    plos_variants = ('PloS one', 'PloS ONE', 'PLOS One',
                     'PloS One', 'PLOS ONE', 'PLOSOne', 'plos one')
    if name in plos_variants:
        return 'PLOS One'
    else:
        return name

for title in titles:
    correct_journal_name(title)
    standardize_plos(title)
