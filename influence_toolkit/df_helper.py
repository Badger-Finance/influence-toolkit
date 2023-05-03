import pandas as pd

from influence_toolkit.constants import POOL_INDEXES
from influence_toolkit.pool_tvls import get_pool_tvls
from influence_toolkit.treasury_captures import get_treasury_captures
from influence_toolkit.aura import aura_mint_ratio
from influence_toolkit.aura import aura_vebal_controlled
from influence_toolkit.aura import get_rel_weights
from influence_toolkit.aura import vebal_controlled_per_aura
from influence_toolkit.convex import get_frax_gauge_weight
from influence_toolkit.vp_info import get_council_vp_fee
from influence_toolkit.vp_info import get_voter_vp


def pct_format(figure):
    return "{0:.1%}".format(figure)


def dollar_format(figure):
    return "${:,.2f}".format(figure)


def display_current_epoch_df():
    # TODO: grab from endpoint tvl in the bunni token
    pools_tvl = [dollar_format(x) for x in get_pool_tvls().append(0)]
    captures = [pct_format(x) for x in get_treasury_captures()]

    balancer_weights = get_rel_weights()
    fxs_weight = get_frax_gauge_weight()
    gauge_rel_weights = [pct_format(x) for x in balancer_weights.append(fxs_weight)]

    df = {
        "Pools": POOL_INDEXES,
        "TVL": pools_tvl,
        "Capture": captures,
        "Gauge Weight": gauge_rel_weights,
    }
    df = pd.DataFrame(df)

    return df.set_index("Pools")


def display_aura_df():
    headers = [
        "Mint Ratio",
        "Treasury VP",
        "Council Fee VP",
        "veBAL per Aura",
        "Aura veBAL controlled",
    ]

    mint_ratio = aura_mint_ratio()
    treasury_votes = get_voter_vp()
    council_fee = get_council_vp_fee()
    vebal_per_aura = vebal_controlled_per_aura()
    aura_vebal_pct = pct_format(aura_vebal_controlled())

    data = [[mint_ratio, treasury_votes, council_fee, vebal_per_aura, aura_vebal_pct]]

    df = pd.DataFrame(data, columns=headers)

    return df
