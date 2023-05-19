import os
from datetime import datetime, timedelta

import pandas as pd
from ape import Contract

from influence_toolkit.constants import CONVEX
from influence_toolkit.constants import CVX_FEE
from influence_toolkit.constants import FXS_DAILY_EMISSIONS
from influence_toolkit.constants import WEEK
from influence_toolkit.constants import FRAX_GAUGE_CONTROLLER
from influence_toolkit.constants import BADGER_FRAXBP_GAUGE
from influence_toolkit.constants import CURVE_GAUGE_CONTROLLER
from influence_toolkit.constants import BADGER_FRAXBP_CURVE_GAUGE


def cvx_mint_ratio():
    """
    Fetches the current minting cvx ratio per crv emitted
    """
    # https://docs.convexfinance.com/convexfinanceintegration/cvx-minting#mint-formula
    cvx = Contract(CONVEX)
    total_cliffs = cvx.totalCliffs()
    cliff_reduction = cvx.reductionPerCliff() / 1e18
    cvx_total_supply = cvx.totalSupply() / 1e18
    current_cliff = cvx_total_supply / cliff_reduction
    remaining_cliffs = total_cliffs - current_cliff
    cvx_mint_ratio = remaining_cliffs / total_cliffs
    return cvx_mint_ratio


def convex_biweekly_emissions(cvx_mint_ratio, cvx_price, crv_price, with_fee=True):
    """
    Calculates the weekly ecosystem usd emissions and returns curve emissions with the
    fee reduction (conditionally) and the total emitted cvx based on the current minting ratio
    """
    # borrow from: https://github.com/Badger-Finance/badger-ape/blob/convex_curve_wars/scripts/convex_curve_wars_votium.py#L29
    schedules = pd.read_csv(
        'https://raw.githubusercontent.com/Badger-Finance/badger-influence-analytics/master/notebooks/cvx_bribes/curve-release-schedule.csv'
    )
    schedules["DateTime"] = pd.date_range("2020-08-13", periods=2190, freq="D")
    schedules = schedules.set_index("DateTime")
    ems_upcoming_round = schedules["Community"].loc[
        (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    ]
    ems_today = schedules["Community"].loc[datetime.now().strftime("%Y-%m-%d")]
    # fee only taken from crv rev: https://docs.convexfinance.com/convexfinance/faq/fees#ed94
    if with_fee:
        round_emissions = (ems_upcoming_round - ems_today) * (1 - CVX_FEE)
    else:
        round_emissions = ems_upcoming_round - ems_today
    biweekly_emissions_curve = round_emissions * crv_price
    biweekly_emissions_convex = round_emissions * cvx_mint_ratio * cvx_price
    return biweekly_emissions_curve, biweekly_emissions_convex


def frax_weekly_emissions(fxs_price):
    """
    Calculates the weekly fxs emissions in usd denomination
    reducing the convex fee out of the FXS portion
    """
    emissions_usd = FXS_DAILY_EMISSIONS * fxs_price * WEEK
    # https://docs.convexfinance.com/convexfinance/faq/fees#convex-for-frax
    weekly_emissions_after_fee = emissions_usd * (1 - CVX_FEE)
    return weekly_emissions_after_fee


def get_frax_gauge_weight():
    """
    Returns the badger/fraxbp gauge relative current weight in Frax ecosystem
    """
    # contracts
    controller = Contract(FRAX_GAUGE_CONTROLLER)

    rel_weight = controller.gauge_relative_weight(BADGER_FRAXBP_GAUGE) / 1e18

    return rel_weight


def get_badger_fraxbp_curve_gauge_weight():
    """
    Returns the badger/fraxbp gauge relative current weight in Curve ecosystem
    """
    # contracts
    controller = Contract(CURVE_GAUGE_CONTROLLER)

    rel_weight = controller.gauge_relative_weight(BADGER_FRAXBP_CURVE_GAUGE) / 1e18

    return rel_weight
