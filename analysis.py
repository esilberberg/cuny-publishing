import pandas as pd

df = pd.read_excel(
    r'/Users/mari_cardenas/Desktop/faculty productivity/output-exp.xlsx')

df['journal'].str.strip()

print(df['journal'].value_counts()) 

# df = df['journal'].value_counts().rename_axis('journal').to_frame('counts')
# print (df)

df = df['journal'].value_counts().rename_axis('journal').reset_index(name='counts')
print (df)


df.to_excel('analysis.xlsx', index=False, encoding='utf-8-sig')

