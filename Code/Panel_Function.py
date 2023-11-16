
'''
As inputs of the following panel function:
- data:the dataset to be converted
- name: The name or full directory with which the panelized dataset will be saved (for example: 'Panel.csv')
'''
# Panel Function

import pandas as pd
import numpy as np

def panel(data, name):
    
    problem_orgs = [' Inc.', ' LLC', ' Inc ', ' LLP ', ' LLP', ' Ltd.', ' P.C.', ' L.P.', ' LP ', ' Inc', ' LP', ' S.A.', ' PC ', ' PLLC', ' plc ']
    
    leadership_id = []
    first_name = []
    last_name = []
    title = []
    org_name = []
    start_date = []
    end_date = []
    full_jobs = []
    other_current = []
    
    #Panelization on past careers
    
    df = data.drop_duplicates('Leadership People Id') # Dropping any duplicates of 'Leadership People Id'
    df = df[df['Careers'].notnull()].reset_index() # Selection of a sub dataset with non null careers for panelization

    for i in tqdm(range(len(df['Careers']))): # Generation of a new line for each past career
        
        leadership_id.append(df.loc[i, 'Leadership People Id'])
        first_name.append(df.loc[i, 'First Name'])
        last_name.append(df.loc[i, 'Last Name'])
        title.append(df.loc[i, 'Title'])
        org_name.append(df.loc[i, 'Organization Name (Parent)'])
        full_jobs.append(str(df.loc[i, 'Title']) + ', ' + str(df.loc[i, 'Organization Name (Parent)']))
        start_date.append(df.loc[i, 'Start Date'])
        end_date.append(None)
        other_current.append(0)
        
        l = df.loc[i, 'Careers'].split(';') #Split of 'Çareers' into the single past careers
        for j in range(len(l)):
            
            l2 = l[j].split(',') # Split of the single career into Title (l2[0]) and Organization Name + Dates (l2[-1])
            
            if l2[-1][:2] == '  ':
                pass
            
            else:
                
                full_jobs.append(l[j])
                if l2[-1][:5] in problem_orgs or l2[-1][:4] in problem_orgs or l2[-1][:3] in problem_orgs: 
                    new = ['', '']
                    new[0] = l2[0]
                    new[1] = ''.join(l2[-2:])
                    l2 = new

                #Generation of the columns
                leadership_id.append(df.loc[i, 'Leadership People Id'])
                first_name.append(df.loc[i, 'First Name'])
                last_name.append(df.loc[i, 'Last Name'])
                title.append(l2[0])

                if '(' not in l2[-1]: #Then neither a start date nor an end date
                    org_name.append(l2[-1])
                    start_date.append(None)
                    end_date.append(None)
                else:
                    if l2[-1][-6] == '(': #Only start date
                        org_name.append(l2[-1][:-6])
                        start_date.append(l2[-1][-5:-1])
                        end_date.append(None)
                    else: #Both start and end date
                        org_name.append(l2[-1][:-11])
                        start_date.append(l2[-1][-10:-6])
                        end_date.append(l2[-1][-5:-1])
                other_current.append(0)
            
    #Panelization on other current roles

    df = data.drop_duplicates('Leadership People Id') # Dropping any duplicates of 'Leadership People Id'
    df = df[df['Other Current Roles'].notnull()].reset_index()
    
    for k in tqdm(range(len(df['Other Current Roles']))): # Generation of a new line for each other current role
        
        if str(df.loc[k, 'Careers']) == 'nan':
            leadership_id.append(df.loc[k, 'Leadership People Id'])
            first_name.append(df.loc[k, 'First Name'])
            last_name.append(df.loc[k, 'Last Name'])
            title.append(df.loc[k, 'Title'])
            org_name.append(df.loc[k, 'Organization Name (Parent)'])
            full_jobs.append(str(df.loc[k, 'Title']) + ', ' + str(df.loc[k, 'Organization Name (Parent)']))
            start_date.append(df.loc[k, 'Start Date'])
            end_date.append(None)
            other_current.append(0) 
        
        l = df.loc[k,'Other Current Roles'].split(';') #Split of 'Other Current Roles' into the single current roles
        for h in range(len(l)):
            
            l2 = l[h].split(',') # Split of the single career into Title (l2[0]) and Organization Name + Dates (l2[-1])

            if l2[-1][:2] == '  ':
                pass
            
            else:
                
                full_jobs.append(l[h])
                if l2[-1][:5] in problem_orgs or l2[-1][:4] in problem_orgs or l2[-1][:3] in problem_orgs: 
                    new = ['', '']
                    new[0] = l2[0]
                    new[1] = ''.join(l2[-2:])
                    l2 = new

                #Generation of the columns
                leadership_id.append(df.loc[k,'Leadership People Id'])
                first_name.append(df.loc[k,'First Name'])
                last_name.append(df.loc[k,'Last Name'])
                title.append(l2[0])
                start_date.append(df.loc[k,'Start Date'])
                end_date.append(None)
                org_name.append(l2[-1])
                other_current.append(1)
            
    
    #Generation of the dataframe with the generated columns
    df3 = pd.DataFrame()
    df3['Leadership People Id'] = leadership_id
    df3['First Name'] = first_name
    df3['Last Name'] = last_name
    df3['Title'] = title
    df3['Organization Name (Parent)'] = org_name
    df3['Full Job'] = full_jobs
    df3['Start Date'] = start_date
    df3['End Date'] = end_date
    df3['Other Current'] = other_current
    
    df = data[(data['Careers'].notnull()) | (data['Other Current Roles'].notnull())]
    df = df.rename({'Start Date':'Current Start Date'}, axis = 1)
    
    #The new dataset is merged with the original dataset to keep all the other time invariant individuals' characteristics
    cols_2 = ['Leadership People Id'] + list(set(df.columns) - set(df3.columns))
    df5 = pd.merge(df.loc[:, cols_2], df3, on = 'Leadership People Id')
    final_cols = list(data.columns) + ['Full Job', 'Current Start Date', 'Other Current', 'End Date']
    df5 = df5[final_cols]
    
    # Finally, the new dataset is concatenated with the observations from the original dataset whose 'Careers' and 'Other Current Roles' column is null, which
    # have only their current career and no past career neither other current roles (thus no need of panelization)
    df4 = data.drop_duplicates('Leadership People Id')
    final_df = pd.concat([df5, df4[(df4['Careers'].isnull()) & (df4['Other Current Roles'].isnull())]])
    final_df.to_csv(name)
