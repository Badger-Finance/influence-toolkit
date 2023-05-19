import requests

from influence_toolkit.constants import BALANCER_SUBGRAPH
from influence_toolkit.constants import SNAPSHOT_SUBGRAPH
from influence_toolkit.constants import CURVE_FACTORY_URL
from influence_toolkit.constants import POOL_ID_BADGER
from influence_toolkit.constants import POOL_ID_DIGG
from influence_toolkit.constants import POOL_ID_BADGER_RETH
from influence_toolkit.constants import CURVE_BADGER_FRAXBP_POOL


PROPOSAL_INFO_QUERY = """
        query($proposal_id: String) {
          proposal(id: $proposal_id) {
            scores_total
            snapshot
            choices
            scores
          }
        }
        """

TVL_QUERY = """
        query($pool_id: String) {
          pool(id: $pool_id) {
            totalLiquidity
          }
        }
        """


def get_proposal_info(proposal_id):
    response_proposal = requests.post(
        SNAPSHOT_SUBGRAPH,
        json={"query": PROPOSAL_INFO_QUERY, "variables": {"proposal_id": proposal_id}},
    ).json()["data"]["proposal"]

    return response_proposal


def get_tvl_balancer_badger_pool():
    response_tvl_badger = requests.post(
        BALANCER_SUBGRAPH,
        json={"query": TVL_QUERY, "variables": {"pool_id": POOL_ID_BADGER}},
    ).json()
    tvl_badger = float(response_tvl_badger["data"]["pool"]["totalLiquidity"])
    return tvl_badger


def get_tvl_balancer_digg_pool():
    response_tvl_badger = requests.post(
        BALANCER_SUBGRAPH,
        json={"query": TVL_QUERY, "variables": {"pool_id": POOL_ID_DIGG}},
    ).json()
    tvl_badger = float(response_tvl_badger["data"]["pool"]["totalLiquidity"])
    return tvl_badger


def get_tvl_balancer_badgerreth_pool():
    response_tvl_badger = requests.post(
        BALANCER_SUBGRAPH,
        json={"query": TVL_QUERY, "variables": {"pool_id": POOL_ID_BADGER_RETH}},
    ).json()
    tvl_badger = float(response_tvl_badger["data"]["pool"]["totalLiquidity"])
    return tvl_badger


def get_tvl_curve_badgerfraxbp_pool():
    r = requests.get(CURVE_FACTORY_URL).json()
    poolData = r["data"]["poolData"]
    for pool in poolData:
        if pool["address"] == CURVE_BADGER_FRAXBP_POOL:
            tvl = float(pool["usdTotal"])
            break
    return tvl


def get_pool_tvls():
    pool_tvls = [
        get_tvl_balancer_badger_pool(),
        get_tvl_balancer_digg_pool(),
        get_tvl_balancer_badgerreth_pool(),
        get_tvl_curve_badgerfraxbp_pool(),
    ]

    return pool_tvls


# choices which have frax gauges as well
DAO_TARGET_GAUGE = "BADGER+FRAXBP (0x13B8…)"
curve_gauge_with_frax_gauge = [
    "FRAX+USDC (0xDcEF…)",
    "FRAX+FPI (0xf861…)",
    "ETH+frxETH (0xa1F8…)",
    "LUSD+FRAXBP (0x497C…)",
    "ApeUSD+FRAXBP (0x04b7…)",
    "GUSD+FRAXBP (0x4e43…)",
    "BUSD+FRAXBP (0x8fdb…)",
    "alUSD+FRAXBP (0xB30d…)",
    "USDD+FRAXBP (0x4606…)",
    "TUSD+FRAXBP (0x33ba…)",
    "PUSd+FRAXBP (0xC47E…)",
    "DOLA+FRAXBP (0xE571…)",
    "agEUR+FRAXBP (0x5825…)",
    "CVX+FRAXBP (0xBEc5…)",
    "cvxCRV+FRAXBP (0x31c3…)",
    "cvxFXS+FRAXBP (0x21d1…)",
    "ALCX+FRAXBP (0x4149…)",
    "MAI+FRAXBP (0x66E3…)",
    DAO_TARGET_GAUGE,
    "RSR+FRAXBP (0x6a62…)",
]


def get_vefxs_mirror_weight(current_proposal_details):
    choices = current_proposal_details["choices"]
    badgerfraxbp_index = choices.index(DAO_TARGET_GAUGE)
    relevant_indexes = []
    for index, choice in enumerate(choices):
        if choice in curve_gauge_with_frax_gauge:
            relevant_indexes.append(index)

    scores = current_proposal_details["scores"]
    score_badgerfraxbp = scores[badgerfraxbp_index]
    scores_total = 0

    for index, score in enumerate(scores):
        if index in relevant_indexes:
            scores_total += score

    weight = score_badgerfraxbp / scores_total

    # reduce the weight, since convex will have some discretionary voting at their end
    # discretion "voting" considered unknown as it is mix with curve gauge voting
    return weight * 0.95
