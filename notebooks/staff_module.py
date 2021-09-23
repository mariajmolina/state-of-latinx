import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt

"""

Module contains several functions for preprocessing staff IPEDS data (https://nces.ed.gov/ipeds/).

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
        if '_f.' in co:
            clean_cols.append(co.split('_f.')[1])
        elif '_f_RV.' in co:
            clean_cols.append(co.split('_f_RV.')[1])
        elif '_F.' in co:
            clean_cols.append(co.split('_F.')[1])
        elif '_F_RV.' in co:
            clean_cols.append(co.split('_F_RV.')[1])
        elif '_IS.' in co:
            clean_cols.append(co.split('_IS.')[1])
        elif '_IS_RV.' in co:
            clean_cols.append(co.split('_IS_RV.')[1])
        else:
            clean_cols.append(co)
            
    return clean_cols

def redo_staff_category(df):
    """
    Changing name of staff column to one consistent name.
    
    Args:
        df: pandas dataframe
    """
    rename = []

    for i in df['Instructional staff category']: 
        
        if 'Instruction/research/public service, ' in i:
            rename.append(i.split('Instruction/research/public service, ')[1].lower())
            
        elif 'Instruction/research/public servicey, ' in i:
            rename.append(i.split('Instruction/research/public servicey, ')[1].lower())
            
        else:
            rename.append(i.lower())
            
    df['Instructional staff category']=rename
    
    return df

def synthesize_staff_categories(df):
    """
    Changing staff categories to consistent naming due to 2000 versus 2010 changes.
    
    Args:
        df: pandas dataframe
    """
    rename_staff_positions = {
            'tenured total':                                           'tenured total', 
            'tenured, professors':                                     'tenured, professors',
            'tenured, instructors':                                    'tenured, instructors',
            'tenured, associate professors':                           'tenured, associate professors',
            'tenured, assistant professors':                           'tenured, assistant professors',
            'tenured, lecturers':                                      'tenured, lecturers',
            'tenured, no academic rank':                               'tenured, no academic rank', 
            'non-tenured on tenure track, professors':                 'on-tenure track, professors',
            'non-tenured on tenure track, associate professors':       'on-tenure track, associate professors',
            'non-tenured on tenure track, assistant professors':       'on-tenure track, assistant professors',
            'non-tenured on tenure track, instructors':                'on-tenure track, instructors', 
            'non-tenured on tenure track total':                       'on-tenure track total',
            'non-tenured on tenure track, lecturers':                  'on-tenure track, lecturers',
            'non-tenured on tenure track, no academic rank':           'on-tenure track, no academic rank',
            'non-tenured not on tenure track total':                   'not on tenure track/no tenure system system total',
            'non-tenured not on tenure track, professors':             'not on tenure/no tenure system, professors',
            'non-tenured not on tenure track, lecturers':              'not on tenure/no tenure system, lecturers',
            'non-tenured not on tenure track, associate professors':   'not on tenure/no tenure system, associate professors',
            'non-tenured not on tenure track, assistant professors':   'not on tenure/no tenure system, assistant professors',
            'non-tenured not on tenure track, instructors':            'not on tenure/no tenure system, instructors',
            'non-tenured not on tenure track, no academic rank':       'not on tenure/no tenure system, no academic rank',}
    
    df['Instructional staff category'] = [rename_staff_positions[i] for i in df['Instructional staff category']]
    
    return df

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
    df = df[df.columns.drop(list(df.filter(regex='IDX_HR')))]
    df = df[df.columns.drop(list(df.filter(regex='unitid')))]
    df = df[df.columns.drop(list(df.filter(regex='- new')))]
    df = df[df.columns.drop(list(df.filter(regex='- old')))]
    
    df.columns = redo_columns(df)
    
    year = df['year'].iloc[0].astype(str)
    
    # renaming columns due to changes in classifications
    if year == '2009' or year == '2010' or year == '2011':
        
        df = df.rename(columns=
                  {"American Indian or Alaska Native total - derived": "American Indian or Alaska Native total",
                   "American Indian or Alaska Native men - derived": "American Indian or Alaska Native men",
                   "American Indian or Alaska Native women - derived": "American Indian or Alaska Native women",
                   "Black or African American/Black non-Hispanic total - derived": "Black or African American total",
                   "Black or African American/Black non-Hispanic men - derived": "Black or African American men",
                   "Black or African American/Black non-Hispanic women - derived": "Black or African American women",
                   "Hispanic or Latino/Hispanic total - derived": "Hispanic or Latino total",
                   "Hispanic or Latino/Hispanic men - derived":   "Hispanic or Latino men",
                   "Hispanic or Latino/Hispanic women - derived": "Hispanic or Latino women",
                   "White/White non-Hispanic total - derived":    "White total",
                   "White/White non-Hispanic men - derived":      "White men",
                   "White/White non-Hispanic women - derived":    "White women",
                   "Tenure status and academic rank of full-time instruction/research/public service staff":"Instructional staff category",
                           })
        
    df = redo_staff_category(df)
    
    if year == '2009' or year == '2010' or year == '2011':
        
        df = synthesize_staff_categories(df)
    
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
    
    df = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7, df8, df9, df10], 
                   keys=[year0, year1, year2, year3, year4, 
                         year5, year6, year7, year8, year9, year10], 
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

def different_tracks(df):
    """
    Filter physical sciences degree programs.
    """
    return df.loc[(df['Instructional staff category'] == 'tenured total') |
                  (df['Instructional staff category'] == 'on-tenure track total') |
                  (df['Instructional staff category'] == 'not on tenure track/no tenure system system total')]

def tenured_positions(df):
    """
    Filter physical sciences degree programs.
    """
    return df.loc[(df['Instructional staff category'] == 'tenured, professors') |
                  (df['Instructional staff category'] == 'tenured, associate professors') |
                  (df['Instructional staff category'] == 'tenured, assistant professors') |
                  (df['Instructional staff category'] == 'tenured, instructors') |
                  (df['Instructional staff category'] == 'tenured, lecturers') |
                  (df['Instructional staff category'] == 'tenured, no academic rank')]

def ontenuretrack_positions(df):
    """
    Filter physical sciences degree programs.
    """
    return df.loc[(df['Instructional staff category'] == 'on-tenure track, professors') |
                  (df['Instructional staff category'] == 'on-tenure track, associate professors') |
                  (df['Instructional staff category'] == 'on-tenure track, assistant professors') |
                  (df['Instructional staff category'] == 'on-tenure track, instructors') |
                  (df['Instructional staff category'] == 'on-tenure track, lecturers') |
                  (df['Instructional staff category'] == 'on-tenure track, no academic rank')]

def notenure_positions(df):
    """
    Filter physical sciences degree programs.
    """
    return df.loc[(df['Instructional staff category'] == 'not on tenure/no tenure system, professors') |
                  (df['Instructional staff category'] == 'not on tenure/no tenure system, associate professors') |
                  (df['Instructional staff category'] == 'not on tenure/no tenure system, assistant professors') |
                  (df['Instructional staff category'] == 'not on tenure/no tenure system, instructors') |
                  (df['Instructional staff category'] == 'not on tenure/no tenure system, lecturers') |
                  (df['Instructional staff category'] == 'not on tenure/no tenure system, no academic rank')]

def full_professor(df):
    """
    Filter physical sciences degree programs.
    """
    return df.loc[(df['Instructional staff category'] == 'tenured, professors') |
                  (df['Instructional staff category'] == 'on-tenure track, professors') |
                  (df['Instructional staff category'] == 'not on tenure/no tenure system, professors')]

def associate_professor(df):
    """
    Filter physical sciences degree programs.
    """
    return df.loc[(df['Instructional staff category'] == 'tenured, associate professors') |
                  (df['Instructional staff category'] == 'on-tenure track, associate professors') |
                  (df['Instructional staff category'] == 'not on tenure/no tenure system, associate professors')]

def assistant_professor(df):
    """
    Filter physical sciences degree programs.
    """
    return df.loc[(df['Instructional staff category'] == 'tenured, assistant professors') |
                  (df['Instructional staff category'] == 'on-tenure track, assistant professors') |
                  (df['Instructional staff category'] == 'not on tenure/no tenure system, assistant professors')]
