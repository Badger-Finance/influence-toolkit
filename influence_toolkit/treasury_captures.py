from ape import Contract

from influence_toolkit.constants import TREASURY_VAULT_MSIG
from influence_toolkit.constants import PRIVATE_VAULT_BADGER_FRAXBP_TREASURY
from influence_toolkit.constants import BADGER_WBTC_POOL
from influence_toolkit.constants import BADGER_RETH_POOL
from influence_toolkit.constants import DIGG_WBTC_GRAVI_POOL
from influence_toolkit.constants import REWARDS_BADGER_WBTC
from influence_toolkit.constants import REWARDS_BADGER_RETH
from influence_toolkit.constants import REWARDS_DIGG_WBTC_GRAVI
from influence_toolkit.constants import CURVE_BADGER_FRAXBP_LP
from influence_toolkit.constants import BADGER_FRAXBP_GAUGE
from influence_toolkit.constants import BUNNI_WBTC_BADGER_GAUGE


def get_treasury_captures():
    # contracts
    pool_badger_wbtc = Contract(BADGER_WBTC_POOL)
    pool_badger_reth = Contract(BADGER_RETH_POOL)
    pool_digg_gravi = Contract(DIGG_WBTC_GRAVI_POOL)
    badger_fraxbp_lp = Contract(CURVE_BADGER_FRAXBP_LP)

    reward_badger_wbtc = Contract(REWARDS_BADGER_WBTC)
    reward_badger_reth = Contract(REWARDS_BADGER_RETH)
    reward_digg_gravi = Contract(REWARDS_DIGG_WBTC_GRAVI)
    gauge_badger_fraxbp = Contract(BADGER_FRAXBP_GAUGE)
    gauge_bunni = Contract(BUNNI_WBTC_BADGER_GAUGE)

    # pool supplies
    ps_badger_wbtc = pool_badger_wbtc.totalSupply() / 1e18
    ps_badger_reth = pool_badger_reth.totalSupply() / 1e18
    ps_digg_gravi = pool_digg_gravi.totalSupply() / 1e18
    ps_badger_fraxbp = badger_fraxbp_lp.totalSupply() / 1e18
    ps_bunni_gauge = gauge_bunni.totalSupply() / 1e18

    # treasury holdings
    vault_badger_wbtc_bal = reward_badger_wbtc.balanceOf(TREASURY_VAULT_MSIG) / 1e18
    vault_badger_reth_bal = reward_badger_reth.balanceOf(TREASURY_VAULT_MSIG) / 1e18
    vault_digg_gravi = reward_digg_gravi.balanceOf(TREASURY_VAULT_MSIG) / 1e18
    vault_badger_fraxbp = (
        gauge_badger_fraxbp.lockedLiquidityOf(PRIVATE_VAULT_BADGER_FRAXBP_TREASURY)
        / 1e18
    )
    vault_bunni_gauge = gauge_bunni.balanceOf(TREASURY_VAULT_MSIG) / 1e18

    # captures
    capture_badger_wbtc = vault_badger_wbtc_bal / ps_badger_wbtc
    capture_badger_reth = vault_badger_reth_bal / ps_badger_reth
    capture_digg_gravi = vault_digg_gravi / ps_digg_gravi
    capture_badger_fraxbp = vault_badger_fraxbp / ps_badger_fraxbp
    capture_bunni_gauge = vault_bunni_gauge / ps_bunni_gauge

    return [
        capture_badger_wbtc,
        capture_digg_gravi,
        capture_badger_reth,
        capture_badger_fraxbp,
        capture_bunni_gauge,
    ]
