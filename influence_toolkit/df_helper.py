import pandas as pd

from influence_toolkit.constants import POOL_INDEXES
from influence_toolkit.pool_tvls import get_pool_tvls
from influence_toolkit.treasury_captures import get_treasury_captures


def pct_format(figure):
    return "{0:.1%}".format(figure)


def dollar_format(figure):
    return "${:,.2f}".format(figure)


def display_df():
    pools_tvl = [dollar_format(x) for x in get_pool_tvls()]
    captures = [0.2, 0.3, 0.4, 0.6]

    df = {"Pools": POOL_INDEXES, "TVL": pools_tvl, "Capture": captures}
    df = pd.DataFrame(df)
    df.set_index("Pools")

    return df
