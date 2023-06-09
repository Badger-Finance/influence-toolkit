from ape import Contract

from influence_toolkit.constants import BADGER_DELEGATE
from influence_toolkit.constants import COUNCIL_FEE
from influence_toolkit.constants import VLAURA
from influence_toolkit.constants import VOTER_MSIG


def get_council_vp_fee():
    strat_votes = Contract(VLAURA).getVotes(BADGER_DELEGATE) / 1e18
    council_fee = strat_votes * COUNCIL_FEE
    return council_fee


def get_voter_vp():
    return Contract(VLAURA).getVotes(VOTER_MSIG) / 1e18
