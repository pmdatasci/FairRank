# ---------------------------------------------------------------
#  PMC_generate_ML_100k_csv.py
# 
#  Create a csv file froma dataset and format it for 
#  recommender system usage.
#
#   Author: Paul McKie    Date: 15-May-2021
# --------------------------------------------------------------- 

import os
import sys

import numpy as np
import pandas as pd


def clean_index(df):
    '''
    - changes the key column to a row number.
    - keeps index if it had a name and is hence (most likely) a column
    - does not set the datatype of the index col as it moves into the df
    '''
    verbose = False
    
    # if the index has a name then we keep it as a column
    if df.index.name is None:
        drop_flag = True
    else:
        if verbose:
            print(f'INDEX has a name: {df.index.name}')
        drop_flag = False
        
    # now reset the index.  dropping or keeping index has been taken care of.    
    df.reset_index(inplace=True, drop=drop_flag)
   
    
    return df

def set_new_index(df, key_col):
    '''
    - clean the index first
    - check if required column in in df (after cleaning)
    - return re-indexed df
    '''
    verbose = False
        
    df = clean_index(df)
    
    if key_col in df.columns.to_list():
        if verbose:
            print(f'setting index. key column in df. all ok')
        df.set_index(key_col, inplace=True, drop=True)
    else:
        print(f'setting index incomplete. key column NOT in df.')
        print(f'COLUMNS: {df.columns.to_list()}  KEY_COL NOT FOUND: {key_col}')
        
    assert(df is not None)
        
    return df

def filter_cols(df, cols_to_keep):
    ''' 
    - assumes index is to be kept.
    - keps only columns in passed in list
    - empty list or no matches ...returns no columns
    - if any columns is NOT in list no error will be reported 
    '''
    
    _cols = df.columns.to_list()
    _cols_returned = []
    
    for col in _cols:
        if col in cols_to_keep:
            _cols_returned.append(col)
    
    df_returned = df[_cols_returned].copy()
    
    return df_returned



def join_datasets(df_p, df_s, key_col_p, key_col_s, cols_to_add_s):
    ''' 
    join supplementary columns from df_s (supplementary data) to df_p (primary) 
        join dataframes on key_col_p with key_col_s.
        add only the columns in list "cols_to_add_s"

    returns a supplemented dataset -> df    
    '''
    df = None
    
    df_p = set_new_index(df_p, key_col_p)
    df_s = set_new_index(df_s, key_col_s)
    
    # only add requested columns
    df_s = filter_cols(df_s, cols_to_add_s)
    
    # produce the merged df
    df = df_p.merge(df_s, left_on=key_col_p, right_on=key_col_s, suffixes=(False, False))

    return df

def get_data_config():
    '''
    - loads a list of dicts that contain the configuration details of the datasets
    
    - currently loads three dictionaries for this dataset
    
    - The first dict in the list is the base dataset.  
      All subsequent datasets are merged with this BASE data.
      
    - Each dict contains {'name': name[i],
                          'file_path': file_path[i],
                          'cols': cols[i],
                          'cols_add': cols_add[i],
                          'key_col': key_col[i], 
                          'sep': sep[i], 
                          'na_values': na_values[i] })
                          
    '''
    verbose = False
        
    # the empty list of dataset configs
    rec_data = []
    n_entries = 3
    
    # the name of the dataset/file     
    name = []
    name.append('user')
    name.append('rating')
    name.append('item')
    assert(len(name) == n_entries)
    
    # path to the dataset
    file_path = []
    file_path.append(os.path.join('~', '.surprise_data', 'ml-100k', 'ml-100k', 'u.data'))
    file_path.append(os.path.join('~', '.surprise_data', 'ml-100k', 'ml-100k', 'u.user'))
    file_path.append(os.path.join('~', '.surprise_data', 'ml-100k', 'ml-100k', 'u.item'))
    assert(len(file_path) == n_entries)
    
    # columns expected to be loaded in the file
    # must be a complete list to much No of cols... files have no headers
    cols = []
    cols.append(['user_id','movie_id','rating','timestamp'])
    cols.append(['user_id','age','gender','occupation','zip code'])
    cols.append(['movie_id','movie title','release date','video release date',
                 'IMDb URL','unknown','Action','Adventure','Animation',
                 'Childrens','Comedy','Crime','Documentary','Drama','Fantasy',
                 'Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi',
                 'Thriller','War','Western'])
    assert(len(cols) == n_entries)
    
    # the columns to add when or supplemnet in the combined dataset
    cols_add = []
    cols_add.append(['user id','movie id','rating','timestamp'])
    cols_add.append(['user_id','age','gender','occupation','zip code'])
    cols_add.append(['movie title','release date','unknown','Action','Adventure','Animation',
                 'Childrens','Comedy','Crime','Documentary','Drama','Fantasy',
                 'Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi',
                 'Thriller','War','Western'])
    assert(len(cols_add) == n_entries)
    
    # the key col that wil be used to join this datset to the BASE                
    key_col = []
    key_col.append('user_id')
    key_col.append('user_id')
    key_col.append('movie_id')
    assert(len(key_col) == n_entries)
    
    # separator for the fiel to be used by read_csv
    sep = []
    sep.append('\t')
    sep.append('|')
    sep.append('|')
    assert(len(sep) == n_entries)
    
    # list of na values to be sued by read_csv
    na_values = []
    na_values.append([])
    na_values.append([])
    na_values.append([])
    assert(len(na_values) == n_entries)
    
    # now add each item
    for i, n in enumerate(name):
        if verbose:
            print(f'Adding {n} to list of data files.')
        rec_data.append({'name':name[i],
                         'file_path': file_path[i],
                         'cols': cols[i],
                         'cols_add': cols_add[i],
                         'key_col':key_col[i], 
                         'sep':sep[i], 
                         'na_values':na_values[i] })

    return rec_data

def get_data(option ='ALL'):
    '''
    - call get data and 
    '''
    verbose = True
    
    # load the list of dicts that describe the datasets
    data_cfg = get_data_config()
    
    # create an empty list of dfs to hold datasets
    dfs = []
    _df= None

    # iterate through the list of dicts and call 'pd.read_csv'
    # to lad all the dfs
    for n in data_cfg:
        name = n.get('name')
        if option=='ALL' or name in option:
            if verbose:
                print(f'Reading Data .. {name} to list of data files.')
            _df = pd.read_csv(n.get('file_path'),  sep = n.get('sep','|'), engine='python', 
                            header=None, names=n.get('cols'),
                            na_values=n.get('na_values', []))
            dfs.append(_df)
    
    # base df
    df_p = dfs[0]
    r,c = df_p.shape
    
    # check that we have data
    assert(r >0)
    
    # now iterate over the dfs to 
    #   join base df with all subsequent dfs
    for i, df_s in enumerate(dfs):
        if i > 0:
            if verbose:
                print(data_cfg[i].get('key_col'))
            new_df = join_datasets(df_p = df_p, 
                                   df_s = df_s,
                                   key_col_p = data_cfg[i].get('key_col'),
                                   key_col_s = data_cfg[i].get('key_col'), 
                                   cols_to_add_s = data_cfg[i].get('cols_add'))
            df_p = new_df.copy()
    
    
    # now reindx with a simple row-number and return
    df_p = clean_index(df_p)
  
    return df_p

def main(file_name):

    try:
        df = get_data('item')
        # df = filter_cols(df, ['movie_id','Action'])

    except IOError as err:
        print("IOError: {}".format(err))
        print("To use this class, please download the following files:")
        print("\n\t ref to movie lens dataset")
        print("\nand place them, as-is, in the folder:")
        print("\n\t{}\n".format(os.path.abspath(os.path.join(
            os.path.abspath(__file__), '~', '.surprise_data', 'ml-100k', 'ml-100k'))))
        sys.exit(1)

    df = filter_cols(df, ['movie_id', 'Action','Adventure','Animation',
                            'Childrens','Comedy','Crime','Documentary',
                            'Drama','Fantasy','Film-Noir','Horror',
                            'Musical','Mystery','Romance','Sci-Fi','Thriller',
                            'War','Western'])
    # df['target'] = df['gender'].replace({'M':1, 'F':0})
    # df = df.query('age > 0 & age < 100')

    print(df.head())
    df.to_csv(file_name, index=False)


    return


if __name__ == "__main__":

    dataset_name = 'ML_100k'
    # filepath = os.path.join('~', 'RMIT', 'data', dataset_name + '.csv')
    filepath = os.path.join('~', 'RMIT','RMITRepo','FairRank', 'datasets', dataset_name + '.csv')
    main(filepath)

