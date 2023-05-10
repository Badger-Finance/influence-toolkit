from decimal import Decimal

from ape import Contract, chain

from influence_toolkit.constants import TREASURY_VAULT_MSIG
from influence_toolkit.constants import TROPS_MSIG
from influence_toolkit.constants import BADGER
from influence_toolkit.constants import BALANCER_BRIBER_HH
from influence_toolkit.constants import AURA_BRIBER_HH
from influence_toolkit.constants import FRAX_BRIBER_HH
from influence_toolkit.constants import BUNNI_BRIBER_HH
from influence_toolkit.constants import BADGER_WBTC_BALANCER_PROPOSAL
from influence_toolkit.constants import BADGER_RETH_BALANCER_PROPOSAL
from influence_toolkit.constants import BADGER_FRAXBP_FRAX_PROPOSAL
from influence_toolkit.constants import BADGER_WBTC_BUNNI_PROPOSAL
from influence_toolkit.constants import SECONDS_PER_BLOCK
from influence_toolkit.constants import WEEK


def _get_incentives_per_market(briber_contract, start_block):
    df = Contract(briber_contract).DepositBribe.query(
        "transaction_hash",
        "block_number",
        "token",
        "proposal",  # NOTE: use to identify which gauge was incentivised
        "amount",
        "briber",
        start_block=start_block,
    )
    df = df[(df["token"] == BADGER) & df["briber"].isin([TROPS_MSIG, TREASURY_VAULT_MSIG])]
    df["Amount"] = df["amount"] / Decimal("1e18")
    df["Proposal"] = df["proposal"].apply(lambda x: x.hex())

    return df


def get_incentives_cost(badger_price):
    # we cap reading for 2w back
    current_block = chain.blocks.height
    blocks_per_week = 60 * 60 * 24 * WEEK / SECONDS_PER_BLOCK
    start_block = current_block - (blocks_per_week * 2)

    # grab cost from all HH marketplaces in the past 2w
    df_balancer_hh = _get_incentives_per_market(BALANCER_BRIBER_HH, start_block)
    # df_aura_hh = _get_incentives_per_market(AURA_BRIBER_HH, start_block)
    # df_frax_hh = _get_incentives_per_market(FRAX_BRIBER_HH, start_block)
    df_bunni_hh = _get_incentives_per_market(BUNNI_BRIBER_HH, start_block)

    # filter incentives per gauge
    wbtc_badger_balancer_incentives = df_balancer_hh[
        df_balancer_hh["Proposal"] == BADGER_WBTC_BALANCER_PROPOSAL
    ]["Amount"].iloc[0]
    badger_reth_balancer_incentives = df_balancer_hh[
        df_balancer_hh["Proposal"] == BADGER_RETH_BALANCER_PROPOSAL
    ]["Amount"].iloc[0]
    badger_wbtc_bunni_incentives = df_bunni_hh[
        df_bunni_hh["Proposal"] == BADGER_WBTC_BUNNI_PROPOSAL
    ]["Amount"].iloc[0]

    # NOTE: assume some of them zero for now for testing
    return [
        wbtc_badger_balancer_incentives * badger_price,
        0,
        badger_reth_balancer_incentives * badger_price,
        0,
        badger_wbtc_bunni_incentives * badger_price,
    ]
