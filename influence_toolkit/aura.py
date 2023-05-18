from ape import Contract

from influence_toolkit.constants import AURA
from influence_toolkit.constants import AURA_FEE
from influence_toolkit.constants import BALANCER_EMISSIONS
from influence_toolkit.constants import POOL_ID_DIGG
from influence_toolkit.constants import PROXY_AURA_VOTER
from influence_toolkit.constants import VEBAL
from influence_toolkit.constants import BALANCER_GAUGE_CONTROLLER
from influence_toolkit.constants import BALANCER_BADGER_WBTC_GAUGE
from influence_toolkit.constants import BALANCER_DIGG_GRAVI_GAUGE
from influence_toolkit.constants import BALANCER_BADGER_RETH_GAUGE
from influence_toolkit.constants import VLAURA


def aura_mint_ratio():
    """
    Fetches the current minting aura ratio per bal emitted
    """
    aura = Contract(AURA)
    total_cliffs = aura.totalCliffs()
    cliff_reduction = aura.reductionPerCliff() / 1e18
    aura_total_supply = aura.totalSupply() / 1e18
    init_mint_amount = aura.INIT_MINT_AMOUNT() / 1e18
    aura_mint_ratio = (
        (total_cliffs - (aura_total_supply - init_mint_amount) / cliff_reduction) * 2.5 + 700
    ) / total_cliffs
    return aura_mint_ratio


def weekly_emissions_after_fee(aura_mint_ratio, bal_price, aura_price):
    """
    Calculates the weekly ecosystem usd emissions and returns balancer emissions
    with the fee reduction and the total emitted aura based on the current minting ratio
    """
    # NOTE: fee is uniquely taken out from the base protocol asset
    weekly_emissions_bal_after_fee = BALANCER_EMISSIONS * bal_price * (1 - AURA_FEE)
    weekly_emissions_aura_after_fee = BALANCER_EMISSIONS * aura_mint_ratio * aura_price
    return weekly_emissions_bal_after_fee, weekly_emissions_aura_after_fee


def aura_vebal_controlled():
    """
    Fetches the amount of veBAL controlled by Aura
    """
    # contracts
    vebal = Contract(VEBAL)

    # calcs
    voter_proxy_aura_vebal_vp = vebal.balanceOf(PROXY_AURA_VOTER) / 1e18

    ts_vebal = vebal.totalSupply() / 1e18

    return voter_proxy_aura_vebal_vp / ts_vebal


def vebal_controlled_per_aura():
    """
    Calculates one much veBal is controlled per AURA
    """
    # contracts
    vebal = Contract(VEBAL)
    vlAURA = Contract(VLAURA)

    # calcs
    voter_proxy_aura_vebal_vp = vebal.balanceOf(PROXY_AURA_VOTER) / 1e18

    ts_vlaura = vlAURA.totalSupply() / 1e18

    vebal_controlled_per_aura = voter_proxy_aura_vebal_vp / ts_vlaura

    return vebal_controlled_per_aura


def get_rel_weights():
    """
    Retrieves the relative current weight for three of the DAO's gauges:
    badger/wbtc, badger/reth and digg/wbtc/gravi
    """
    # contracts
    gauge_controller = Contract(BALANCER_GAUGE_CONTROLLER)

    weight_badger_wbtc = gauge_controller.gauge_relative_weight(BALANCER_BADGER_WBTC_GAUGE) / 1e18
    weight_digg_gravi = gauge_controller.gauge_relative_weight(BALANCER_DIGG_GRAVI_GAUGE) / 1e18
    weight_badger_reth = gauge_controller.gauge_relative_weight(BALANCER_BADGER_RETH_GAUGE) / 1e18

    return [weight_badger_wbtc, weight_digg_gravi, weight_badger_reth]


def get_rel_weight_reducted(total_vebal_vp):
    """
    Calculates the rel.weight of specific gauge deducting a specific
    amount of vebal voting weight (coming from treasury & council fees)
    """
    # contracts
    gauge_controller = Contract(BALANCER_GAUGE_CONTROLLER)

    gauge_weight = gauge_controller.get_gauge_weight(BALANCER_BADGER_WBTC_GAUGE) / 1e18
    total_weight = gauge_controller.get_total_weight() / 1e18

    real_weight_bought = gauge_weight - total_vebal_vp

    return real_weight_bought / total_weight


def get_gravi_in_balancer_pool(balancer_vault):
    """
    Fetches the current amount of graviAURA deposited in
    the digg/wbtc/gravi pool
    """
    digg_pool_info = balancer_vault.getPoolTokens(POOL_ID_DIGG)
    gravi_in_digg_pool = digg_pool_info[1][2] / 1e18
    return gravi_in_digg_pool
