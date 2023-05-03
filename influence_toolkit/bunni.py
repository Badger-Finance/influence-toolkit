from ape import Contract

from influence_toolkit.constants import BUNNI_GAUGE_CONTROLLER
from influence_toolkit.constants import BUNNI_WBTC_BADGER_GAUGE
from influence_toolkit.constants import BUNNI_EXERCISE_DISCOUNT
from influence_toolkit.constants import BUNNI_WEEKLY_EMISSIONS


def get_bunni_gauge_weight():
    controller = Contract(BUNNI_GAUGE_CONTROLLER)

    rel_weight = controller.gauge_relative_weight(BUNNI_WBTC_BADGER_GAUGE) / 1e18

    return rel_weight


def get_bunni_weekly_emissions(lit_price):
    weekly_emissions = BUNNI_WEEKLY_EMISSIONS * lit_price

    # discounted
    discounted_weekly_emissions = weekly_emissions * BUNNI_EXERCISE_DISCOUNT

    return discounted_weekly_emissions
