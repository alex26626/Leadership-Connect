import pandas as pd
import numpy as np
import matplotilib.pyplot as plt

'''
The following function takes a comparison dataset as an input, and it prints the following match rates:
- % of positive pairs: The % of names for which at least one downloaded image is correct.
- % of negative pairs: The % of names for which none of the downloaded images is correct.
- Average Prediction: Considering only positive pairs, it's the average number of correct images per person.
- Percentage of first predictions: Considering only positive pairs, it's the % of times the first downloaded image is correct.
'''

def match_rates(data_set):
    data_set.loc[:, 'Label Prediction'] = data_set.apply(lambda x: 1 if x['Prediction'] is True else 0, axis = 1)
    dataset_aggregate = data_set.groupby('Name').sum(numeric_only = True)
    tot = dataset_aggregate.shape[0]
    is_null = dataset_aggregate[dataset_aggregate['Label Prediction'].isnull()].shape[0]
    not_null = dataset_aggregate[dataset_aggregate['Label Prediction'].notnull()].shape[0]
    positive = dataset_aggregate[dataset_aggregate['Label Prediction'] > 0].shape[0]
    negative = dataset_aggregate[dataset_aggregate['Label Prediction'] == 0].shape[0]

    print('% of null comparisons: ', str(is_null*100/tot))
    print('% of positive pairs: ', str(positive*100/not_null))
    print('% of negative pairs: ', str(negative*100/not_null))


    dataset_positive = dataset_aggregate[dataset_aggregate['Label Prediction'] > 0]
    print('Average Prediction: ', int(dataset_positive['Label Prediction'].sum())/dataset_positive.shape[0])

    try:
      data_set.loc[:, 'First'] = data_set.apply(lambda x: 1 if x['File Name'].split('_')[1][0] == str(0) else 0, axis = 1)
    except:
      data_set.loc[:, 'First'] = data_set.apply(lambda x: 1 if x['File Name'].split('.')[0][-1] == str(0) else 0, axis = 1)
    dataset_first = data_set[data_set['First'] == 1]
    print('Percentage of first predictions: ', dataset_first['Label Prediction'].mean()*100)

'''
The following function computes and prints the match rates defined above for majority voting. It takes as inputs:
- combination_directory: The directory to the combination file.
- comparison_directory: The directory to the comparison file.
- threshold: The threshold for majority voting. For instance, if threshold = 3, then the match rates will be computed only for names for which at least 3
among the downloaded images are the same.
In addition to the match rates defined above, the function also computes the Sample Proportion, which is the percentage of names left after applying the threshold.
For instance, if threshold = 3, and Sample Proportion = 30%, then for 30% of the people at least 3 images are the same (contain the same person).
'''

def sub_match_rates(combination_directory, comparison_directory, threshold):
  combinations = pd.read_csv(combination_directory).drop('Unnamed: 0', axis = 1)
  combinations['Prediction'] = combinations['Prediction']*1
  combinations_agg = combinations.groupby('Name').sum(numeric_only = False).reset_index()
  match_names = list(set(combinations_agg.loc[combinations_agg['Prediction'] >= threshold, 'Name']))
  comparison = pd.read_csv(comparison_directory).drop('Unnamed: 0', axis = 1)
  match_linkedin_5 = comparison[comparison['Name'].isin(match_names)]
  print('Sample Proportion: ', len(match_names)*100/len(set(comparison['Name'])))
  match_rates(match_linkedin_5)

'''
The following function takes as inputs an origin dataset and a comparison dataset, and it outputs three graphs:
- Positive Origins: The most frequent sources among positive pairs, in decreasing order, with their relative frequency.
- Negative Origins: The most frequent sources among negative pairs, in decreasing order, with their relative frequency.
- Null Origins: The most frequent sources among null pairs (where the downloaded image is not a person), in decreasing order, with their relative frequency.
'''

def origins_analysis(origins_data, comparisons_data):
  origins_comparison = pd.merge(origins_data, comparisons_data, on = 'File Name')
  positive_origins = origins_comparison[origins_comparison['Prediction'] == True].reset_index(drop = True)
  null_origins = origins_comparison[origins_comparison['Prediction'].isnull()].reset_index(drop = True)
  negative_origins = origins_comparison[origins_comparison['Prediction'] == False].reset_index(drop = True)

  positive_origins_count = positive_origins.groupby('Origin').count().reset_index().loc[:, ['Origin', 'File Name']].rename({'File Name':'Num'}, axis = 1).sort_values('Num', ascending = False).reset_index(drop = True)
  positive_origins_count['Frequency'] = positive_origins_count['Num']*100/positive_origins_count['Num'].sum()
  positive_origins_count = positive_origins_count.iloc[:10, :]

  negative_origins_count = negative_origins.groupby('Origin').count().reset_index().loc[:, ['Origin', 'File Name']].rename({'File Name':'Num'}, axis = 1).sort_values('Num', ascending = False).reset_index(drop = True)
  negative_origins_count['Frequency'] = negative_origins_count['Num']*100/negative_origins_count['Num'].sum()
  negative_origins_count = negative_origins_count.iloc[:10, :]

  null_origins_count = null_origins.groupby('Origin').count().reset_index().loc[:, ['Origin', 'File Name']].rename({'File Name':'Num'}, axis = 1).sort_values('Num', ascending = False).reset_index(drop = True)
  null_origins_count['Frequency'] = null_origins_count['Num']*100/null_origins_count['Num'].sum()
  null_origins_count = null_origins_count.iloc[:10, :]

  plt.figure(figsize = (15,4))

  plt.subplot(1,3,1)
  plt.bar(positive_origins_count['Origin'], positive_origins_count['Frequency'])
  plt.xticks(rotation = 90)
  plt.title('Positive Origins')
  plt.xlabel('Origins')
  plt.ylabel('Frequency')

  plt.subplot(1,3,2)
  plt.bar(negative_origins_count['Origin'], negative_origins_count['Frequency'])
  plt.xticks(rotation = 90)
  plt.title('Negative Origins')
  plt.xlabel('Origins')
  plt.ylabel('Frequency')

  plt.subplot(1,3,3)
  plt.bar(null_origins_count['Origin'], null_origins_count['Frequency'])
  plt.xticks(rotation = 90)
  plt.title('Null Origins')
  plt.xlabel('Origins')
  plt.ylabel('Frequency')
  plt.show()
