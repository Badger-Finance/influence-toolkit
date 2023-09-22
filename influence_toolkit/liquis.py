from ape import Contract

from influence_toolkit.constants import VELIT
from influence_toolkit.constants import LIQ
from influence_toolkit.constants import VLLIQ
from influence_toolkit.constants import PROXY_LIQUIS_VOTER
from influence_toolkit.constants import LIQ_VESTED_ESCROW_TREASURY
from influence_toolkit.constants import VOTER_MSIG
from influence_toolkit.constants import LIQUIS_FEE
from influence_toolkit.constants import BUNNI_EXERCISE_DISCOUNT
from influence_toolkit.constants import BUNNI_WEEKLY_EMISSIONS


def get_liquis_weekly_emissions(liq_mint_ratio, lit_price, liq_price):
    """
    Calculates the weekly ecosystem usd emissions and returns olit emissions
    with the fee reduction and the total emitted liq based on the current minting ratio
    """
    weekly_emissions = BUNNI_WEEKLY_EMISSIONS * lit_price

    # discounted
    discounted_weekly_emissions = weekly_emissions * BUNNI_EXERCISE_DISCOUNT

    weekly_emissions_olit_after_fee = discounted_weekly_emissions * (1 - LIQUIS_FEE)
    weekly_emissions_aura_after_fee = (
        BUNNI_WEEKLY_EMISSIONS * liq_mint_ratio * liq_price
    )

    return weekly_emissions_olit_after_fee, weekly_emissions_aura_after_fee


def liquis_mint_ratio():
    """
    Fetches the current minting liq ratio per olit emitted
    """
    liq = Contract(LIQ)
    total_cliffs = liq.totalCliffs()
    cliff_reduction = liq.reductionPerCliff() / 1e18
    liq_total_supply = liq.totalSupply() / 1e18
    init_mint_amount = liq.INIT_MINT_AMOUNT() / 1e18
    liq_mint_ratio = (
        (total_cliffs - (liq_total_supply - init_mint_amount) / cliff_reduction) * 0.25
        + 70
    ) / total_cliffs
    return liq_mint_ratio


def liq_velit_controlled():
    """
    Fetches the amount of veLIT controlled by Liquis
    and total velit supply
    """
    # contracts
    velit = Contract(VELIT)

    # calcs
    voter_proxy_liquis_velit_vp = velit.balanceOf(PROXY_LIQUIS_VOTER) / 1e18

    ts_velit = velit.totalSupply() / 1e18

    return voter_proxy_liquis_velit_vp / ts_velit, ts_velit


def velit_controlled_per_liq():
    """
    Calculates one much veLIT is controlled per LIQ
    """
    # contracts
    velit = Contract(VELIT)
    vlliq = Contract(VLLIQ)

    # calcs
    voter_proxy_liquis_velit_vp = velit.balanceOf(PROXY_LIQUIS_VOTER) / 1e18

    ts_vlliq = vlliq.totalSupply() / 1e18

    velit_controlled_per_liq = voter_proxy_liquis_velit_vp / ts_vlliq

    return velit_controlled_per_liq


def get_vlliq_treasury_balance():
    """
    Gets the locked vlLIQ from treasury
    """
    vested_escrow = Contract(LIQ_VESTED_ESCROW_TREASURY)

    total_locked = vested_escrow.totalLocked(VOTER_MSIG) / 1e18
    available = vested_escrow.available(VOTER_MSIG) / 1e18

    locked = total_locked - available

    return available
