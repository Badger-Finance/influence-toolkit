from ape import Contract

from influence_toolkit.constants import FRAX_GAUGE_CONTROLLER
from influence_toolkit.constants import BADGER_FRAXBP_GAUGE
from influence_toolkit.constants import CURVE_GAUGE_CONTROLLER
from influence_toolkit.constants import BADGER_FRAXBP_CURVE_GAUGE


def get_frax_gauge_weight():
    # contracts
    controller = Contract(FRAX_GAUGE_CONTROLLER)

    rel_weight = controller.gauge_relative_weight(BADGER_FRAXBP_GAUGE) / 1e18

    return rel_weight


def get_badger_fraxbp_curve_gauge_weight():
    # contracts
    controller = Contract(CURVE_GAUGE_CONTROLLER)

    rel_weight = controller.gauge_relative_weight(BADGER_FRAXBP_CURVE_GAUGE) / 1e18

    return rel_weight
