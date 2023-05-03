from ape import Contract

from influence_toolkit.constants import BUNNI_GAUGE_CONTROLLER
from influence_toolkit.constants import BUNNI_WBTC_BADGER_GAUGE


def get_bunni_gauge_weight():
    controller = Contract(BUNNI_GAUGE_CONTROLLER)

    rel_weight = controller.gauge_relative_weight(BUNNI_WBTC_BADGER_GAUGE) / 1e18

    return rel_weight
