from crossref.restful import Works
import pandas as pd

cuny_keywords = ['CUNY', 'City University of New York', 'Bronx', 'Lehman', 'Queens', 
'Queensborough', 'Brooklyn College', 'Kingsborough', 'Staten Island', 'Baruch', 
'Manhattan', 'BMCC', 'Craig Newmark', 'Graduate Center', 'School of Public Health', 
'Labor and Urban Studies', 'School of Law', 'School of Professional Studies', 'Guttman',
'Hostos', 'Hunter', 'John Jay', 'LaGuardia', 'Medgar Evers', 'College of Technology', 'City College', 'York']

df = pd.read_csv('SoTL-bibliography.csv')

# Start list of author information from Crossref
authors = []

# Get DOIs from CSV file
for doi in df['DOI']:
    if isinstance(doi, str):
        row = []
        row.append(doi)
        print(doi)

        # Create query to Crossref API
        works = Works()
        query = works.doi(doi)

        # Find total number of authors, test if authors' info exists on Crossref, and return that info
        try:
            num_of_authors = len(query['author'])
            for x in range(0, num_of_authors):
                try:
                    given_name = query['author'][x]['given']
                except KeyError:
                    given_name = ''
                try:
                    last_name = query['author'][x]['family']
                except KeyError:
                    given_name = ''
                full_name = f'{given_name} {last_name}'

                # Test if author affiliation exists
                try:
                    affiliation = query['author'][x]['affiliation'][0]['name']
                except IndexError:
                    affiliation = 'affiliation unknown'
                
                # Test if the author is affiliated with CUNY
                if num_of_authors > 1:
                    if any(word in affiliation for word in cuny_keywords):
                        row.append(full_name)
                        row.append(affiliation)
                        print(full_name)
                        print(affiliation)
                else:
                    row.append(full_name)
                    row.append(affiliation)
                    print(full_name)
                    print(affiliation)

        except TypeError:
            row.append('Authors unknown in Crossref')
            print('Authors unknown in Crossref')
        except KeyError:
            row.append('Authors unknown in Crossref')
            print('Authors unknown in Crossref')
    else:
        row.append('DOI not provided')
        print('DOI not provided')

    authors.append(row)

#Print to CSV
df_authors = pd.DataFrame(authors)
df_authors.to_csv('out.csv', encoding='utf-8-sig')
