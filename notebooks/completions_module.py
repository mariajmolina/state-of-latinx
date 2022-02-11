import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt

"""

Module contains several functions for preprocessing degree completions IPEDS data (https://nces.ed.gov/ipeds/).

Author: Maria J. Molina, NCAR (molina@ucar.edu)

"""

def redo_columns(df):
    """
    Removing year label in column names.
    
    Args:
        df: pandas dataframe
    """
    clean_cols = []

    for co in df.columns:
        if '_A.' in co:
            clean_cols.append(co.split('_A.')[1])
        elif '_RV.' in co:
            clean_cols.append(co.split('_RV.')[1])
        else:
            clean_cols.append(co)
            
    return clean_cols

def preprocess(filename):
    """
    Preprocessing of dataframes.
    
    Args:
        filename: string of filename
    """
    df = pd.read_csv(filename)

    # dropping due to inconsistent naming/columns
    df = df[df.columns.drop(list(df.filter(regex='Asian')))]
    df = df[df.columns.drop(list(df.filter(regex='Pacific')))]
    df = df[df.columns.drop(list(df.filter(regex='distance')))]
    df = df[df.columns.drop(list(df.filter(regex='IDX_C')))]
    df = df[df.columns.drop(list(df.filter(regex='unitid')))]
    df = df[df.columns.drop(list(df.filter(regex='- new')))]
    df = df[df.columns.drop(list(df.filter(regex='- old')))]
    
    df.columns = redo_columns(df)
    
    year = df['year'].iloc[0].astype(str)
    
    # renaming columns due to changes in classifications
    if year == '2009' or year == '2010':
        
        df = df.rename(columns=
                  {"American Indian or Alaska Native total - derived": "American Indian or Alaska Native total",
                   "American Indian or Alaska Native men - derived": "American Indian or Alaska Native men",
                   "American Indian or Alaska Native women - derived": "American Indian or Alaska Native women",
                   "Black or African American/Black non-Hispanic total - derived": "Black or African American total",
                   "Black or African American/Black non-Hispanic men - derived": "Black or African American men",
                   "Black or African American/Black non-Hispanic women - derived": "Black or African American women",
                   "Hispanic or Latino/Hispanic total - derived": "Hispanic or Latino total",
                   "Hispanic or Latino/Hispanic men - derived": "Hispanic or Latino men",
                   "Hispanic or Latino/Hispanic women - derived": "Hispanic or Latino women",
                   "White/White non-Hispanic total - derived": "White total",
                   "White/White non-Hispanic men - derived": "White men",
                   "White/White non-Hispanic women - derived": "White women",
                           })
    
    return df, year

def open_and_concat(filelist):
    """
    Open and concatenate the files.
    
    Args:
        filelist: list of filename strings
    """
    df0 , year0  = preprocess(filelist[0])   # 2009
    df1 , year1  = preprocess(filelist[1])
    df2 , year2  = preprocess(filelist[2])
    df3 , year3  = preprocess(filelist[3])
    df4 , year4  = preprocess(filelist[4])
    df5 , year5  = preprocess(filelist[5])
    df6 , year6  = preprocess(filelist[6])
    df7 , year7  = preprocess(filelist[7])
    df8 , year8  = preprocess(filelist[8])
    df9 , year9  = preprocess(filelist[9])
    df10, year10 = preprocess(filelist[10])  # 2019
    df11, year11 = preprocess(filelist[11])
    
    df = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7, 
                    df8, df9, df10, df11], 
                   keys=[year0, year1, year2, year3, year4, 
                         year5, year6, year7, year8, year9, 
                         year10, year11], 
                   sort=False)
    
    return df

def diff(df1, df2, col_name):
    """
    Difference between two dataframe columns.
    
    Args:
        df1: dataframe
        df2: dataframe
        col_name: name of column difference
    """
    temp = pd.DataFrame(df1 - df2)
    temp.columns = [col_name]
    
    return temp

def physical_sciences(df):
    """
    Filter physical sciences degree programs.
    """
    return df.loc[(df['CIP Code -  2000 Classification'] == "'40'") |
                  (df['CIP Code -  2010 Classification'] == "'40'") |
                  (df['CIP Code -  2020 Classification'] == "'40'")]

def atmospheric_sciences(df):
    """
    Filter atmospheric sciences degree programs.
    """
    return df.loc[(df['CIP Code -  2000 Classification'] == "'40.04'") |
                  (df['CIP Code -  2010 Classification'] == "'40.04'") |
                  (df['CIP Code -  2020 Classification'] == "'40.04'")]

def earth_sciences(df):
    """
    Filter Earth sciences degree programs.
    """
    return df.loc[(df['CIP Code -  2000 Classification'] == "'40.06'") |
                  (df['CIP Code -  2010 Classification'] == "'40.06'") |
                  (df['CIP Code -  2020 Classification'] == "'40.06'")]

def earth_and_atmos_sciences(df):
    """
    Filter atmospheric and Earth sciences degree programs.
    """
    return df.loc[(df['CIP Code -  2000 Classification'] == "'40.06'") |
                  (df['CIP Code -  2000 Classification'] == "'40.04'") |
                  (df['CIP Code -  2010 Classification'] == "'40.06'") |
                  (df['CIP Code -  2010 Classification'] == "'40.04'") |
                  (df['CIP Code -  2020 Classification'] == "'40.06'") |
                  (df['CIP Code -  2020 Classification'] == "'40.04'")]

def all_degreesandcerts(df):
    """
    Filter for all degrees and certificates (i.e., select all degrees).
    """
    return df.loc[(df['Award Level code'] == 'Degrees/certificates total')]

def all_degrees(df):
    """
    Filter for all degrees (i.e., select all degrees).
    """
    return df.loc[(df['Award Level code'] == 'Degrees total')]

def bs_degrees(df):
    """
    Filter for BS degrees.
    """
    return df.loc[(df['Award Level code'] == "Bachelor's degree")]

def ms_degrees(df):
    """
    Filter for MS degrees.
    """
    return df.loc[(df['Award Level code'] == "Master's degree")]

def phd_degrees(df):
    """
    Filter for PhD degrees.
    """
    return df.loc[(df['Award Level code'] == "Doctor's degree (old degree classification)") |
                  (df['Award Level code'] == "Doctor's degree - research/scholarship (new degree classification)") |
                  (df['Award Level code'] == "Doctor's degree - other (new degree classification)") |
                  (df['Award Level code'] == "Doctor's degree - research/scholarship") |
                  (df['Award Level code'] == "Doctor's degree - other")]

def bs_to_phd_degrees(df):
    """
    Filter for BS to PhD degrees.
    """
    return df.loc[(df['Award Level code'] == "Doctor's degree (old degree classification)") |
                  (df['Award Level code'] == "Doctor's degree - research/scholarship (new degree classification)") |
                  (df['Award Level code'] == "Doctor's degree - other (new degree classification)") |
                  (df['Award Level code'] == "Doctor's degree - research/scholarship") |
                  (df['Award Level code'] == "Doctor's degree - other") |
                  (df['Award Level code'] == "Master's degree") |
                  (df['Award Level code'] == "Bachelor's degree")]
