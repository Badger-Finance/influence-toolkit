from ape import Contract

from constants import BADGER_DELEGATE
from constants import COUNCIL_FEE
from constants import VLAURA
from constants import VOTER_MSIG


def get_council_vp_fee():
    strat_votes = Contract(VLAURA).getVotes(BADGER_DELEGATE) / 1e18
    council_fee = strat_votes * COUNCIL_FEE
    return council_fee


def get_voter_vp():
    return Contract(VLAURA).getVotes(VOTER_MSIG) / 1e18
