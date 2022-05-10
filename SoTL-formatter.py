import pandas as pd

df = pd.read_csv('scopus1.csv')

# Create APA citation
apa_citation = []

for index, row in df.iterrows():
	author = row['Authors']
	title = row['Title']
	year = row['Year']
	journal = row['Source title']
	vol = row['Volume']
	issue = row['Issue']
	doi = row['Identifier']
	pg_start = row['Page start']
	pg_end = row['Page end']

	# Modify APA format if information is missing
	if pd.isna(row['Volume']):
		journal_issue = ''	
	else: journal_issue = f', {vol}({issue})'

	if pd.isna(row['Issue']):
		journal_issue = ''	
	else: journal_issue = f', {vol}({issue})'

	if pd.isna(row['Page start']):
		page_range = ''
	else: page_range = f', {pg_start}-{pg_end}'

	if pd.isna(row['Identifier']):
		doi = '.'
	else: doi = f'. https://doi.org/{doi}'

	citation = f'{author} ({year}). {title}. {journal}{journal_issue}{page_range}{doi}'
	apa_citation.append(citation)

df['Complete APA Citation'] = apa_citation

# Expand author supplied keywords into multiple columns
df['Author Keywords'].str.split(';', expand=True)
df[['Teaching and Learning Focus Tag 1', 'Teaching and Learning Focus Tag 2', 'Teaching and Learning Focus Tag 4', 'extra tags']] = df['Author Keywords'].str.split(';', 3, expand=True)

# Print to a new CSV file
df.to_csv('SoTL.csv', index=False, encoding='utf-8-sig')


