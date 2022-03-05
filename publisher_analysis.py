import pandas as pd

print('~*~ Publisher Analysis ~*~')
csv = input('Drag and drop csv file here: ')
df = pd.read_csv(csv)

# Part A: General tallies
publisher_count = df['publisher'].nunique()
print(f'Total number of publishers = {publisher_count}')
print('=================')
publications_count = df['count'].sum()
print(f'Total number of publications = {publications_count}')

# Part B: Number of titles (individual journals) per publisher
titles_count = df['publisher'].value_counts()
titles_count.to_csv('titles-per-publisher.csv', index=True, encoding='utf-8-sig')

# Part C: Number of publications (citations) per publisher
publishers = df['publisher'].unique()
publications_per_publisher = {"publisher":[],"total_publications":[]}
for pub in publishers:
    a = df.loc[df['publisher'] == pub, 'count'].sum()
    publications_per_publisher['publisher'].append(pub)
    publications_per_publisher['total_publications'].append(a)

publishers_df = pd.DataFrame(publications_per_publisher, columns = ['publisher','total_publications'])

publishers_df.to_csv('pubs-per-publisher.csv', index=False, encoding='utf-8-sig')