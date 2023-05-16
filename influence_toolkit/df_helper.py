import numpy as np
import pandas as pd

from influence_toolkit.constants import POOL_PLATFORMS, POOLS
from influence_toolkit.pool_tvls import get_pool_tvls
from influence_toolkit.treasury_captures import get_treasury_captures
from influence_toolkit.aura import aura_mint_ratio
from influence_toolkit.aura import weekly_emissions_after_fee
from influence_toolkit.aura import aura_vebal_controlled
from influence_toolkit.aura import get_rel_weights
from influence_toolkit.aura import get_rel_weight_reducted
from influence_toolkit.aura import vebal_controlled_per_aura
from influence_toolkit.bunni import get_bunni_gauge_weight
from influence_toolkit.bunni import get_bunni_weekly_emissions
from influence_toolkit.coingecko import get_aura_prices
from influence_toolkit.coingecko import get_bunni_prices
from influence_toolkit.coingecko import get_badger_price
from influence_toolkit.coingecko import get_convex_prices
from influence_toolkit.convex import cvx_mint_ratio
from influence_toolkit.convex import get_frax_gauge_weight
from influence_toolkit.convex import get_badger_fraxbp_curve_gauge_weight
from influence_toolkit.convex import convex_biweekly_emissions
from influence_toolkit.convex import frax_weekly_emissions
from influence_toolkit.incentives_cost import get_incentives_cost
from influence_toolkit.vp_info import get_council_vp_fee
from influence_toolkit.vp_info import get_voter_vp


# class with enums to avoid magical numbers in conditionals
class Gauges:
    BADGER_WBTC_BALANCER = 0
    DIGG_GRAVI_WBTC_BALANCER = 1
    BADGER_RETH_BALANCER = 2
    BADGER_FRAXBP = 3
    BADGER_WBTC_BUNNI = 4


def pct_format(figure):
    if np.isnan(figure):
        return ""
    return "{0:.1%}".format(figure)


def dollar_format(figure):
    return "${:,.0f}".format(figure)


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
    lvl1_weights = balancer_weights + [curve_weight, np.nan]
    lvl2_weights = [
        np.nan,
        np.nan,
        np.nan,
        np.nan,
        bunni_weight,
    ]  # TODO: add aura/convex weights?
    lvl3_weights = [np.nan, np.nan, np.nan, fxs_weight, np.nan]

    # prices
    bal_price, aura_price = get_aura_prices()
    lit_price = get_bunni_prices()
    badger_price = get_badger_price()
    cvx_price, crv_price, fxs_price = get_convex_prices()

    # ecosystem emissions
    mint_ratio = aura_mint_ratio()
    weekly_emissions_usd = weekly_emissions_after_fee(mint_ratio, bal_price, aura_price)
    biweekly_aura_emissions_usd = weekly_emissions_usd * 2

    cvx_ratio = cvx_mint_ratio()
    # NOTE: in this case we are no deducting the fee here, since for badger/fraxbp fee is only taken in the shape of FXS
    biweekly_convex_emissions_usd = convex_biweekly_emissions(
        cvx_ratio, cvx_price, crv_price, with_fee=False
    )

    biweekly_frax_emissions_usd = frax_weekly_emissions(fxs_price) * 2

    weekly_bunni_emissions = get_bunni_weekly_emissions(lit_price)
    biweekly_bunni_emissions = weekly_bunni_emissions * 2

    # incentive costs
    incentives = get_incentives_cost(badger_price)

    # deduct vp coming from our voter_msig & council fee
    # currently assume all is "hard-coded" into wbtc/badger gauge
    voters_msig_aura_vp = get_voter_vp()
    council_fee_aura_vp = get_council_vp_fee()
    total_aura_vp = voters_msig_aura_vp + council_fee_aura_vp

    vebal_per_aura = vebal_controlled_per_aura()
    total_vebal_vp = total_aura_vp * vebal_per_aura

    # gross revenue estimations
    gross_rev = []
    for idx, capture in enumerate(treasury_captures):
        rel_weight = rel_weights[idx]
        if idx == Gauges.BADGER_WBTC_BUNNI:
            usd_rev = capture * rel_weight * biweekly_bunni_emissions
        elif idx == Gauges.BADGER_FRAXBP:
            # here we include both set of emissions: crv, cvx & fxs
            usd_rev_convex = capture * curve_weight * biweekly_convex_emissions_usd
            usd_rev_frax = capture * fxs_weight * biweekly_frax_emissions_usd
            usd_rev = usd_rev_convex + usd_rev_frax
        else:
            usd_rev = capture * rel_weight * biweekly_aura_emissions_usd
        gross_rev.append(usd_rev)

    # net revenue estimations
    net_revenue = []
    for idx, gross in enumerate(gross_rev):
        if idx == Gauges.BADGER_WBTC_BALANCER:
            rel_weight_reducted = get_rel_weight_reducted(total_vebal_vp)
            net_rev = gross / rel_weights[idx] * rel_weight_reducted
        else:
            net_rev = gross
        net_revenue.append(net_rev)

    # df
    df = {
        "Platform(s)": "",
        "Pool": POOLS,
        "TVL": tvls,
        "Capture": treasury_captures,
        "Lvl1 Gauge": lvl1_weights,
        "Lvl2 Gauge": lvl2_weights,
        "Lvl3 Gauge": lvl3_weights,
        "Gross Revenue": gross_rev,
        "Net Revenue": net_revenue,
        "Cost": incentives,
    }
    df = pd.DataFrame(df)
    df["Platform(s)"] = df["Pool"].map(POOL_PLATFORMS)
    df["ROI"] = (df["Net Revenue"] / df["Cost"]).apply(pct_format)

    # formatting of columns
    df["TVL"] = df["TVL"].apply(dollar_format)
    df["Capture"] = df["Capture"].apply(pct_format)
    df["Lvl1 Gauge"] = df["Lvl1 Gauge"].apply(pct_format)
    df["Lvl2 Gauge"] = df["Lvl2 Gauge"].apply(pct_format)
    df["Lvl3 Gauge"] = df["Lvl3 Gauge"].apply(pct_format)
    df["Gross Revenue"] = df["Gross Revenue"].apply(dollar_format)
    df["Net Revenue"] = df["Net Revenue"].apply(dollar_format)
    df["Cost"] = df["Cost"].apply(dollar_format)

    return df.set_index(["Platform(s)", "Pool"])


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
