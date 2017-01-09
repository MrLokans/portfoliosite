from collections import namedtuple
from typing import Sequence


Contribution = namedtuple('Contribution', 'date count')


class ContributionObtainer(object):

    def __init__(self):
        pass

    def _get_github_user_url(self, username):
        pass

    def get_all_contributions(self, username: str) -> Sequence[Contribution]:
        pass

