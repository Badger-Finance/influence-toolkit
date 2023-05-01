from ape import Contract

from constants import TREASURY_VAULT_MSIG
from constants import BADGER_WBTC_POOL
from constants import BADGER_RETH_POOL
from constants import DIGG_WBTC_GRAVI_POOL
from constants import REWARDS_BADGER_WBTC
from constants import REWARDS_BADGER_RETH
from constants import REWARDS_DIGG_WBTC_GRAVI


def get_treasury_captures():
    pool_badger_wbtc = Contract(BADGER_WBTC_POOL)
    pool_badger_reth = Contract(BADGER_RETH_POOL)
    pool_digg_gravi = Contract(DIGG_WBTC_GRAVI_POOL)

    reward_badger_wbtc = Contract(REWARDS_BADGER_WBTC)
    reward_badger_reth = Contract(REWARDS_BADGER_RETH)
    reward_digg_gravi = Contract(REWARDS_DIGG_WBTC_GRAVI)

    # pool supplies
    ps_badger_wbtc = pool_badger_wbtc.totalSupply() / 1e18
    ps_badger_reth = pool_badger_reth.totalSupply() / 1e18
    ps_digg_gravi = pool_digg_gravi.totalSupply() / 1e18

    # treasury holdings
    vault_badger_wbtc_bal = reward_badger_wbtc.balanceOf(TREASURY_VAULT_MSIG) / 1e18
    vault_badger_reth_bal = reward_badger_reth.balanceOf(TREASURY_VAULT_MSIG) / 1e18
    vault_digg_gravi = reward_digg_gravi.balanceOf(TREASURY_VAULT_MSIG) / 1e18

    # captures
    capture_badger_wbtc = vault_badger_wbtc_bal / ps_badger_wbtc
    capture_badger_reth = vault_badger_reth_bal / ps_badger_reth
    capture_digg_gravi = vault_digg_gravi / ps_digg_gravi

    return capture_badger_wbtc, capture_badger_reth, capture_digg_gravi
