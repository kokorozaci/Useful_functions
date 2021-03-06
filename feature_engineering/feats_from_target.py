import os
import gc
import time
import numpy as np
import pandas as pd


def add_target_agg_features(df, 
                            gpby_cols, 
                            target_col = ['store', 'item'], 
                            agg_funcs={'mean':np.mean, 
                                       'median':np.median, 
                                       'max':np.max,      
                                       'min':np.min, 
                                       'std':np.std}):
    '''
    Creates various target column agg features with given agg functions  
    '''
    gpby = df.groupby(gpby_cols)
    newdf = df[gpby_cols].drop_duplicates().reset_index(drop=True)
    for agg_name, agg_func in agg_funcs.items():
        aggdf = gpby[target_col].agg(agg_func).reset_index()
        aggdf.rename(columns={target_col:target_col+'_'+agg_name}, inplace=True)
        newdf = newdf.merge(aggdf, on=gpby_cols, how='left')
    return newdf
    
 
def add_target_lag_feats(df, 
                         gpby_cols = ['store', 'item'], 
                         target_col, 
                         lags = [1, 3, 7, 14]):

    '''
    Creates various target column lag features with lags  
    '''
    
    gpby = df.groupby(gpby_cols)
    for i in lags:
        df['_'.join([target_col, 'lag', str(i)])] = \
                gpby[target_col].shift(i).values + np.random.normal(scale=1.6, size=(len(df),))
    return df


def create_target_rolling_mean_feats(df, 
                                     gpby_cols = ['store', 'item'], 
                                     target_col, 
                                     windows = [2, 7], 
                                     min_periods=2, 
                             shift=1, win_type=None):
                             
    '''
    Creates  target column rolling mean features 
    '''                         
    
    gpby = df.groupby(gpby_cols)
    for w in windows:
        df['_'.join([target_col, 'rmean', str(w)])] = \
            gpby[target_col].shift(shift).rolling(window=w, 
                                                  min_periods=min_periods,
                                                  win_type=win_type).mean().values)
    return df


def create_target_rolling_median_feats(df, gpby_cols, target_col, 
                                       windows = [2, 7], 
                                       min_periods=2, 
                                       shift=1, 
                                       win_type=None):
                            
    '''
    Creates  target column rolling median features 
    '''  
    
    gpby = df.groupby(gpby_cols)
    for w in windows:
        df['_'.join([target_col, 'rmed', str(w)])] = \
            gpby[target_col].shift(shift).rolling(window=w, 
                                                  min_periods=min_periods,
                                                  win_type=win_type).median().values)
    return df


def create_target_ewm_feats(df, gpby_cols, target_col, alpha=[0.9], shift=[1]):

    '''
    Creates  target column exponentially weighted mean features 
    '''  

    gpby = df.groupby(gpby_cols)
    for a in alpha:
        for s in shift:
            df['_'.join([target_col, 'lag', str(s), 'ewm', str(a)])] = \
                gpby[target_col].shift(s).ewm(alpha=a).mean().values
    return df
