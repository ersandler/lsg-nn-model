"""
File: sankey.py
Description:  A simple library for building sankey diagrams from a dataframe
Author: John Rachlin
Date: etc.
"""
import pandas as pd
import plotly.graph_objects as go
import numpy as np


def _code_mapping(df, src, targ):

    # get the distinct labels from src/targ columns
    labels = list(set(list(df[src]) + list(df[targ])))

    # generate n integers for n labels
    codes = list(range(len(labels)))

    # create a map from label to code
    lc_map = dict(zip(labels, codes))

    # substitute names for codes in the dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    # Return modified dataframe and list of labels
    return df, labels


def stack_columns(df, *cols):
    df_stacked = pd.DataFrame()

    num_cols = len(cols[0])

    for current_col in range(0, num_cols - 1):
        col0 = cols[0][current_col]
        col1 = cols[0][current_col + 1]

        df_current = df[[col0, col1]]
        df_current = df_current.reset_index(drop=True)
        df_current.columns = ['src', 'targ']


        df_stacked = pd.concat([df_stacked, df_current], axis=0)

    df_stacked = df_stacked.groupby(['src', 'targ']).size().reset_index(name='num')
    print(df_stacked)

    return df_stacked

def make_sankey(df, *cols, vals=None, title='', save=None, **kwargs):
    """
    Create a sankey diagram from a dataframe and specified columns
    :type cols:
    :param df:
    :param src:
    :param targ:
    :param vals:
    :param save:
    :param kwargs:
    :return:
    """
    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)

    # stack columns if there are more than 2
    if len(cols) > 2:
        df = stack_columns(df, cols)

    src = 'src'
    targ = 'targ'
    if vals is None:
        values = df['num']




    # convert df labels to integer values
    df, labels = _code_mapping(df, src, targ)

    link = {'source': df[src], 'target': df[targ], 'value': values,
            'line': {'color': 'black', 'width': 1}}

    node_thickness = kwargs.get("node_thickness", 50)

    node = {'label': labels, 'pad': 300, 'thickness': node_thickness,
            'line': {'color': 'black', 'width': 1}}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)

    # For dashboarding, you will want to return the fig
    # rather than show the fig.
    
    fig.update_layout(title_text=title)

    fig.show()
    
    # This requires installation of kaleido library
    # https://pypi.org/project/kaleido/
    # See: https://anaconda.org/conda-forge/python-kaleido
    # conda install -c conda-forge python-kaleido

    if save != None:
        fig.write_image(file=save)