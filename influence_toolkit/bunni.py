import pandas as pd
from ape import Contract

from influence_toolkit.constants import TREASURY_VAULT_MSIG
from influence_toolkit.constants import BUNNI_GAUGE_CONTROLLER
from influence_toolkit.constants import BUNI_WBTC_BADGER_LP_RANGE_2820_13829
from influence_toolkit.constants import BUNNI_WBTC_BADGER_GAUGE
from influence_toolkit.constants import BADGER_WBTC_UNIV3
from influence_toolkit.constants import VELIT
from influence_toolkit.constants import BUNNI_EXERCISE_DISCOUNT
from influence_toolkit.constants import BUNNI_WEEKLY_EMISSIONS


def get_bunni_gauge_weight():
    """
    Fetches the current relative gauge weight for badger/wbtc
    """
    controller = Contract(BUNNI_GAUGE_CONTROLLER)

    rel_weight = controller.gauge_relative_weight(BUNNI_WBTC_BADGER_GAUGE) / 1e18

    return rel_weight


def get_bunni_weekly_emissions(lit_price):
    """
    Calculates the weekly emissions in Bunni ecosystem
    """
    weekly_emissions = BUNNI_WEEKLY_EMISSIONS * lit_price

    # discounted
    discounted_weekly_emissions = weekly_emissions * BUNNI_EXERCISE_DISCOUNT

    return discounted_weekly_emissions


def _staking_weight_formula(
    lp_balance, total_liquidity, velit_balance, velit_supply, tokenless_production
):
    """
    Calculates the staking weight of an user given its LP balance, total liquidity,
    its veLIT balance, current total veLIT supply and tokenless gauge factor
    """
    # https://docs.bunni.pro/docs/tokenomics/boosting#the-bunni-model
    # tcr50 compliant: https://snapshot.org/#/timelessfi.eth/proposal/0xc7408d278e384e11bcb9b41475d4798d89b42ce6f01f7ab7733abd59588e03fa
    factor_total_liq = 1 - tokenless_production
    return min(
        lp_balance,
        tokenless_production * lp_balance
        + factor_total_liq * total_liquidity * (velit_balance / velit_supply),
    )


def get_treasury_bunni_gauge_capture():
    """
    Calculates the treasury gauge capture considering other
    depositors and their velit holdings
    """
    badger_wbtc_gauge = Contract(BUNNI_WBTC_BADGER_GAUGE)
    velit = Contract(VELIT)

    # tokenless factor
    tokenless_factor = badger_wbtc_gauge.tokenless_production() / 100

    # https://etherscan.io/tx/0x46d3fec275ad0d8c3e0895e92aca3cd3f2052bddbe1d4d7f9e0714f489749b53
    gauge_creation_block = 16728734
    # NOTE: `provider` gets mix with rpc so needs to normalise the `event_arguments` instead
    df_deposits = badger_wbtc_gauge.Deposit.query("*", start_block=gauge_creation_block)

    # filter those with `bal > 0` and filter duplicates
    df_depositors = pd.json_normalize(df_deposits["event_arguments"])
    df_depositors = df_depositors.drop_duplicates(subset=["provider"])
    df_depositors["balance"] = df_depositors["provider"].apply(
        lambda x: badger_wbtc_gauge.balanceOf(x)
    )
    df_depositors = df_depositors[df_depositors["balance"] > 0]

    # total supplies
    gauge_supply = badger_wbtc_gauge.totalSupply()
    velit_supply = velit.totalSupply()

    # velit depositor balances
    df_depositors["velit_balance"] = df_depositors["provider"].apply(lambda x: velit.balanceOf(x))

    # calc individual staking weight and total
    df_depositors["staking_weight"] = df_depositors.apply(
        lambda x: _staking_weight_formula(
            x.balance, gauge_supply, x.velit_balance, velit_supply, tokenless_factor
        ),
        axis=1,
    )

    total_staking_weight = df_depositors["staking_weight"].sum()

    treasury_row = df_depositors.query("provider == @TREASURY_VAULT_MSIG")
    treasury_gauge_capture = treasury_row["staking_weight"].iloc[0] / total_staking_weight

    return treasury_gauge_capture


def is_bunni_lp_in_range():
    """
    Compare current univ3 pool tick versus bunni
    lp range [tickLower, tickUpper] and returns
    current price in badger per wbtc denomination
    """
    bunni_lp = Contract(BUNI_WBTC_BADGER_LP_RANGE_2820_13829)
    univ3_pool = Contract(BADGER_WBTC_UNIV3)
    
    lower_tick = bunni_lp.tickLower()
    upper_tick = bunni_lp.tickUpper()

    current_tick = univ3_pool.slot0()[1]
    readable_price = (1.0001 ** current_tick) / 1e10

    if lower_tick <= current_tick and upper_tick >= current_tick:
        return True, readable_price
    
    return False, readable_price


def get_bunni_readable_range():
    """
    Returns the range expressed in
    badger per wbtc denomination
    """
    bunni_lp = Contract(BUNI_WBTC_BADGER_LP_RANGE_2820_13829)

    lower_tick = bunni_lp.tickLower()
    upper_tick = bunni_lp.tickUpper()

    lower_tick_in_badger_per_wbtc = (1.0001 ** lower_tick) / 1e10
    upper_tick_in_badger_per_wbtc = (1.0001 ** upper_tick) / 1e10

    return [lower_tick_in_badger_per_wbtc, upper_tick_in_badger_per_wbtc]