from ape import Contract

from influence_toolkit.constants import AURA
from influence_toolkit.constants import AURA_FEE
from influence_toolkit.constants import BALANCER_EMISSIONS
from influence_toolkit.constants import POOL_ID_DIGG
from influence_toolkit.constants import PROXY_AURA_VOTER
from influence_toolkit.constants import VEBAL
from influence_toolkit.constants import VLAURA


def aura_mint_ratio():
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
    weekly_emissions = (
        BALANCER_EMISSIONS * bal_price + BALANCER_EMISSIONS * aura_mint_ratio * aura_price
    )
    weekly_emissions_after_fee = weekly_emissions * (1 - AURA_FEE)
    return weekly_emissions_after_fee


def vebal_controlled_per_aura():
    # contracts
    vebal = Contract(VEBAL)
    vlAURA = Contract(VLAURA)

    # calcs
    voter_proxy_aura_vebal_vp = vebal.balanceOf(PROXY_AURA_VOTER) / 1e18

    ts_vlaura = vlAURA.totalSupply() / 1e18

    vebal_controlled_per_aura = voter_proxy_aura_vebal_vp / ts_vlaura

    return vebal_controlled_per_aura


def get_gravi_in_balancer_pool(balancer_vault):
    digg_pool_info = balancer_vault.getPoolTokens(POOL_ID_DIGG)
    gravi_in_digg_pool = digg_pool_info[1][2] / 1e18
    return gravi_in_digg_pool
