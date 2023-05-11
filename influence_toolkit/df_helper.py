import pandas as pd

from influence_toolkit.constants import POOL_INDEXES
from influence_toolkit.pool_tvls import get_pool_tvls
from influence_toolkit.treasury_captures import get_treasury_captures
from influence_toolkit.aura import aura_mint_ratio
from influence_toolkit.aura import weekly_emissions_after_fee
from influence_toolkit.aura import aura_vebal_controlled
from influence_toolkit.aura import get_rel_weights
from influence_toolkit.aura import vebal_controlled_per_aura
from influence_toolkit.bunni import get_bunni_gauge_weight
from influence_toolkit.bunni import get_bunni_weekly_emissions
from influence_toolkit.coingecko import get_aura_prices
from influence_toolkit.coingecko import get_bunni_prices
from influence_toolkit.coingecko import get_badger_price
from influence_toolkit.convex import get_frax_gauge_weight
from influence_toolkit.convex import get_badger_fraxbp_curve_gauge_weight
from influence_toolkit.incentives_cost import get_incentives_cost
from influence_toolkit.vp_info import get_council_vp_fee
from influence_toolkit.vp_info import get_voter_vp


def pct_format(figure):
    return "{0:.1%}".format(figure)


def dollar_format(figure):
    return "${:,.2f}".format(figure)


def display_current_epoch_df():
    # TODO: grab from endpoint tvl in the bunni token in usd
    tvls = get_pool_tvls() + [0]

    # captures
    treasury_captures = get_treasury_captures()

    # rel.weights
    balancer_weights = get_rel_weights()
    fxs_weight = get_frax_gauge_weight()
    curve_weight = get_badger_fraxbp_curve_gauge_weight()
    bunni_weight = get_bunni_gauge_weight()
    rel_weights = balancer_weights + [fxs_weight, bunni_weight]
    gauge_rel_weights = [pct_format(x) for x in rel_weights]
    # NOTE: trying to sneak dirt-ily the curve rel.weight
    # TODO: make this a separate column
    gauge_rel_weights[3] += f", {pct_format(curve_weight)}"

    # prices
    bal_price, aura_price = get_aura_prices()
    lit_price = get_bunni_prices()
    badger_price = get_badger_price()

    # ecosystem emissions
    mint_ratio = aura_mint_ratio()
    weekly_emissions_usd = weekly_emissions_after_fee(mint_ratio, bal_price, aura_price)
    biweekly_emissions_usd = weekly_emissions_usd * 2

    # TODO: crunch same figures for fxs/convex
    weekly_bunni_emissions = get_bunni_weekly_emissions(lit_price)
    biweekly_bunni_emissions = weekly_bunni_emissions * 2

    # incentive costs
    incentives = get_incentives_cost(badger_price)

    # revenue estimations
    rev_estimations = []
    for idx, capture in enumerate(treasury_captures):
        rel_weight = rel_weights[idx]
        if idx == 4:
            usd_rev = capture * rel_weight * biweekly_bunni_emissions
        else:
            usd_rev = capture * rel_weight * biweekly_emissions_usd
        rev_estimations.append(usd_rev)

    # df
    df = {
        "Pools": POOL_INDEXES,
        "TVL": tvls,
        "Capture": treasury_captures,
        "Gauge Weight": gauge_rel_weights,
        "Estimated Revenue": rev_estimations,
        "Cost": incentives,
    }
    df = pd.DataFrame(df)
    df["TVL"] = df["TVL"].apply(dollar_format)
    df["Capture"] = df["Capture"].apply(pct_format)
    # df["Gauge Weight"] = df["Gauge Weight"].apply(pct_format)  # TODO: need curve column fix first
    df["Estimated Revenue"] = df["Estimated Revenue"].apply(dollar_format)
    df["Cost"] = df["Cost"].apply(dollar_format)
    df["ROI"] = (df["Estimated Revenue"] / df["Cost"] - 1).apply(pct_format)

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
