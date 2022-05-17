from crossref.restful import Works
import pandas as pd

cuny_keywords = ['CUNY', 'City University of New York', 'Bronx', 'Lehman', 'Queens', 
'Queensborough', 'Brooklyn College', 'Kingsborough', 'Staten Island', 'Baruch', 
'Manhattan', 'BMCC', 'Craig Newmark', 'Graduate Center', 'School of Public Health', 
'Labor and Urban Studies', 'School of Law', 'School of Professional Studies', 'Guttman',
'Hostos', 'Hunter', 'John Jay', 'LaGuardia', 'Medgar Evers', 'College of Technology', 'City College', 'York']

df = pd.read_csv(r'C:\Users\erics\Desktop\SoTL-bibliography.csv')

# Get DOIs from CSV file
for d in df['DOI']:
    if isinstance(d, str):
        doi = d
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
                        print(full_name)
                        print(affiliation)
                else:
                    print(full_name)
                    print(affiliation)

        except TypeError:
            print('Authors unknown in Crossref')
        except KeyError:
            print('Authors unknown in Crossref')
    else:
        print('DOI not provided--------------------------')