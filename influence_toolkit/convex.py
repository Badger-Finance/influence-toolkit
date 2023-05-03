from ape import Contract

from influence_toolkit.constants import FRAX_GAUGE_CONTROLLER
from influence_toolkit.constants import BADGER_FRAXBP_GAUGE


def get_frax_gauge_weight():
    # contracts
    controller = Contract(FRAX_GAUGE_CONTROLLER)

    rel_weight = controller.gauge_relative_weight(BADGER_FRAXBP_GAUGE) / 1e18

    return rel_weight
