import pandas as pd


def pct_format(figure):
    return "{0:.1%}".format(figure)


def dollar_format(figure):
    return "${:,.2f}".format(figure)


def display_df(labels, values):
    data = [values]
    headers = labels
    df = pd.DataFrame(data, columns=headers)
    return df
