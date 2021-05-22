import pandas as pd

df = pd.read_csv('./datasets/GermanCredit_sex.csv')

_min = df['CreditAmount'].min()
_max = df['CreditAmount'].max()
print(df.head())

print(f'Min: {_min}  Max: {_max}')

print(df.sort_values(by=['CreditAmount'], ascending=False).head(5))
print(df.sort_values(by=['CreditAmount'], ascending=True).head(5))