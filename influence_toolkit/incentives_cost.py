from decimal import Decimal

from ape import Contract, chain

from influence_toolkit.constants import TREASURY_VAULT_MSIG
from influence_toolkit.constants import TROPS_MSIG
from influence_toolkit.constants import BADGER
from influence_toolkit.constants import LIQ
from influence_toolkit.constants import BRIBE_VAULT_V2
from influence_toolkit.constants import BALANCER_BRIBER_HH
from influence_toolkit.constants import AURA_BRIBER_HH
from influence_toolkit.constants import FRAX_BRIBER_HH
from influence_toolkit.constants import BUNNI_BRIBER_HH
from influence_toolkit.constants import QUEST_BOARD_VELIQ
from influence_toolkit.constants import BADGER_WBTC_BALANCER_PROPOSAL
from influence_toolkit.constants import BADGER_RETH_BALANCER_PROPOSAL
from influence_toolkit.constants import BADGER_FRAXBP_FRAX_PROPOSAL
from influence_toolkit.constants import BADGER_WBTC_BUNNI_PROPOSAL
from influence_toolkit.constants import BADGER_WBTC_LIQUIS_PROPOSAL
from influence_toolkit.constants import SECONDS_PER_BLOCK
from influence_toolkit.constants import WEEK


def _get_incentives_per_market(briber_contract, start_block):
    """
    Retrieves `DepositBribe` and `NewQuest` events from the `briber_contract`
    starting from block height provided in the argument `start_block`
    """
    if briber_contract == QUEST_BOARD_VELIQ:
        quest_board = Contract(briber_contract)
        df = quest_board.NewQuest.query(
            "transaction_hash",
            "block_number",
            "creator",
            "questID",
            "rewardToken",
            start_block=start_block,
        )
        df = df[
            (df["rewardToken"].isin([BADGER, LIQ]))
            & df["creator"].isin([TROPS_MSIG, TREASURY_VAULT_MSIG])
        ]
        df["Amount"] = df["questID"].apply(
            lambda x: quest_board.quests(x).totalRewardAmount / Decimal("1e18")
        )
        df["Proposal"] = BADGER_WBTC_LIQUIS_PROPOSAL
    else:
        df = Contract(briber_contract).DepositBribe.query(
            "transaction_hash",
            "block_number",
            "token",
            "proposal",  # NOTE: use to identify which gauge was incentivised
            "amount",
            "briber",
            start_block=start_block,
        )
        df = df[
            (df["token"] == BADGER)
            & df["briber"].isin([TROPS_MSIG, TREASURY_VAULT_MSIG])
        ]
        df["Amount"] = df["amount"] / Decimal("1e18")
        df["Proposal"] = df["proposal"].apply(lambda x: x.hex())

    return df


def get_incentives_cost(badger_price, liq_price):
    """
    Calculates the incentive cost in usd from the past round
    for different markets in HH & Paladin
    """
    # we cap reading for 2w-3w back, depending on market
    current_block = chain.blocks.height
    blocks_per_week = 60 * 60 * 24 * WEEK / SECONDS_PER_BLOCK
    start_block_balancer = current_block - (blocks_per_week * 2)
    # NOTE: there may be the ocassion of having the bunni incentive
    # 3w back whenever we run this method
    start_block_bunni = current_block - (blocks_per_week * 3)

    # grab cost from all HH marketplaces in the past 2w
    # df_balancer_hh = _get_incentives_per_market(BRIBE_VAULT_V2, start_block_balancer)
    # df_aura_hh = _get_incentives_per_market(AURA_BRIBER_HH, start_block_balancer)
    # df_frax_hh = _get_incentives_per_market(FRAX_BRIBER_HH, start_block)
    df_bunni_hh = _get_incentives_per_market(BRIBE_VAULT_V2, start_block_bunni)
    df_paladin = _get_incentives_per_market(QUEST_BOARD_VELIQ, start_block_bunni)

    # filter incentives per gauge
    """
    wbtc_badger_balancer_incentives = 0
    if (
        len(
            df_balancer_hh[df_balancer_hh["Proposal"] == BADGER_WBTC_BALANCER_PROPOSAL][
                "Amount"
            ]
        )
        > 0  # NOTE: in some rounds we may not incentive this marketplace
    ):
        wbtc_badger_balancer_incentives = df_balancer_hh[
            df_balancer_hh["Proposal"] == BADGER_WBTC_BALANCER_PROPOSAL
        ]["Amount"].iloc[0]

    badger_reth_balancer_incentives = 0
    if (
        len(
            df_balancer_hh[df_balancer_hh["Proposal"] == BADGER_RETH_BALANCER_PROPOSAL][
                "Amount"
            ]
        )
        > 0  # NOTE: in some rounds we may not incentive this marketplace
    ):
        badger_reth_balancer_incentives = df_balancer_hh[
            df_balancer_hh["Proposal"] == BADGER_RETH_BALANCER_PROPOSAL
        ]["Amount"].iloc[0]
    """
    
    badger_wbtc_bunni_incentives = 0
    if (
        len(
            df_bunni_hh[df_bunni_hh["Proposal"] == BADGER_WBTC_BUNNI_PROPOSAL]["Amount"]
        )
        > 0  # NOTE: in some rounds we may not incentive this marketplace
    ):
        badger_wbtc_bunni_incentives = df_bunni_hh[
            df_bunni_hh["Proposal"] == BADGER_WBTC_BUNNI_PROPOSAL
        ]["Amount"].iloc[0]

    badger_wbtc_liquis_incentives = 0
    if (
        len(df_paladin[df_paladin["Proposal"] == BADGER_WBTC_LIQUIS_PROPOSAL]["Amount"])
        > 0  # NOTE: in some rounds we may not incentive this marketplace
    ):
        badger_wbtc_liquis_incentives = df_paladin[
            df_paladin["Proposal"] == BADGER_WBTC_LIQUIS_PROPOSAL
        ]["Amount"].sum()

    # NOTE: assume some of them zero for now for testing
    return [
        (float(wbtc_badger_balancer_incentives) + float(df_aura_hh["Amount"].sum()))
        * badger_price,
        float(0),
        float(badger_reth_balancer_incentives) * badger_price,
        float(0),
        float(badger_wbtc_bunni_incentives) * badger_price
        + float(badger_wbtc_liquis_incentives) * liq_price,
    ]
