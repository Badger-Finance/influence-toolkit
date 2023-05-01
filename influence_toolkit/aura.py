from influence_toolkit.constants import AURA_FEE
from influence_toolkit.constants import BALANCER_EMISSIONS
from influence_toolkit.constants import POOL_ID_DIGG


def aura_mint_ratio(aura):
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


def get_gravi_in_balancer_pool(balancer_vault):
    # digg pool id
    digg_pool_info = balancer_vault.getPoolTokens(POOL_ID_DIGG)
    gravi_in_digg_pool = digg_pool_info[1][2] / 1e18
    return gravi_in_digg_pool
