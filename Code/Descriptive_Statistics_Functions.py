import pandas as pd
import numpy as np

'''
This function computes the percentage of null observations for each column. It takes a dataset as the unique input.
'''
def null_perc(d):
    nums = []
    for i in range(len(d.columns)):
        perc = len(d.loc[d[d.columns[i]].isnull(), d.columns[i]])*100/len(d[d.columns[i]])
        nums.append(perc)
    d1 = pd.DataFrame()
    d1['Columns'] = d.columns
    d1['Null'] = nums
    d1 = d1.sort_values('Null', ascending = False).set_index('Columns')
    return d1

'''
This function computes the relative frequency of observations for each category of the specified column. It takes two inputs:
- d: The dataset.
- column: The name of the column, it needs to be a string.
'''

def stats(d, column):
    d1 = pd.DataFrame(d.groupby(column).count()['Leadership People Id']).rename({'Leadership People Id':'Count'}, axis = 1).sort_values('Count', ascending = False)
    tot = d1['Count'].sum()
    d1['%'] = d1['Count']*100/tot
    return d1

'''
This function returns the absolute and relative frequencies of the top 30 observations for each column of the specified dataset.
'''

def top_30(data):
    freq_final = pd.DataFrame()
    for i in range(len(data.columns)):
        col = data.columns[i]
        if col != 'Leadership People Id':
            freq = pd.DataFrame()
            dm = data.groupby(col).count().reset_index()[[col, 'Leadership People Id']].sort_values('Leadership People Id', ascending = False)
            if len(dm[col]) > 30:
                freq[col] = dm.loc[:30, col]
                freq[f'{col}_freq'] = dm.loc[:30, 'Leadership People Id']
                freq.reset_index(drop = True, inplace = True)
                freq.loc[30, col] = 'Other'
                freq.loc[30, f'{col}_freq'] = dm.loc[:30, 'Leadership People Id'].sum()
                freq[f'{col}_perc'] = freq[f'{col}_freq']*100/freq[f'{col}_freq'].sum()
                freq.reset_index(drop = True, inplace = True)
                freq_final = pd.concat([freq_final, freq], axis = 1)
            else:
                freq[col] = dm[col]
                freq[f'{col}_freq'] = dm['Leadership People Id']
                freq[f'{col}_perc'] = freq[f'{col}_freq']*100/freq[f'{col}_freq'].sum()
                freq.reset_index(drop = True, inplace = True)
                freq_final = pd.concat([freq_final, freq], axis = 1)
            

    return freq_final.iloc[:31, :]
