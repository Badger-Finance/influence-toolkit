import pandas as pd
from ape import Contract

from influence_toolkit.constants import TREASURY_VAULT_MSIG
from influence_toolkit.constants import BUNNI_GAUGE_CONTROLLER
from influence_toolkit.constants import BUNNI_WBTC_BADGER_GAUGE
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


def _staking_weight_formula(lp_balance, total_liquidity, velit_balance, velit_supply):
    """
    Calculates the staking weight of an user given its LP balance, total liquidity,
    its veLIT balance and current total veLIT supply
    """
    # https://docs.bunni.pro/docs/tokenomics/boosting#the-bunni-model
    return min(
        lp_balance,
        0.1 * lp_balance + 0.9 * total_liquidity * (velit_balance / velit_supply),
    )


def get_treasury_bunni_gauge_capture():
    """
    Calculates the treasury gauge capture considering other
    depositors and their velit holdings
    """
    badger_wbtc_gauge = Contract(BUNNI_WBTC_BADGER_GAUGE)
    velit = Contract(VELIT)

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
    df_depositors["velit_balance"] = df_depositors["provider"].apply(
        lambda x: velit.balanceOf(x)
    )

    # calc individual staking weight and total
    df_depositors["staking_weight"] = df_depositors.apply(
        lambda x: _staking_weight_formula(
            x.balance, gauge_supply, x.velit_balance, velit_supply
        ),
        axis=1,
    )

    total_staking_weight = df_depositors["staking_weight"].sum()

    treasury_row = df_depositors.query("provider == @TREASURY_VAULT_MSIG")
    treasury_gauge_capture = (
        treasury_row["staking_weight"].iloc[0] / total_staking_weight
    )

    return treasury_gauge_capture
