import pandas as pd

csv = 'publications-2020.csv'

df = pd.read_csv(csv)

df = df['school'].value_counts().rename_axis(
    'school').reset_index(name='publications')

df.to_excel('school-count.xlsx', index=False, encoding='utf-8-sig')
