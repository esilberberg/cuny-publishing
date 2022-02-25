import pandas as pd

# Tallies the number of publications per school
print('~*~ SCHOOL COUNT ~*~')
print('csv file must contain columns labeled <school> and <publications>')
print('copy and past path to csv file:')
csv = input()


df = pd.read_csv(csv)

df = df['school'].value_counts().rename_axis(
    'school').reset_index(name='publications')

df.to_csv('school-count.csv', index=False, encoding='utf-8-sig')
