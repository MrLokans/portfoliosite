import datetime
import itertools
import logging
from typing import Sequence
from urllib.parse import urlencode

import requests

from bs4 import BeautifulSoup
from bs4.element import Tag


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Contribution(object):

    __slots__ = ('date', 'count')

    def __init__(self, date: datetime.datetime, count: int):
        self.date = date
        self.count = count

    def __repr__(self):
        return 'Contribution(date={}, count={})'.format(self.date, self.count)

    def __eq__(self, other):
        return self.date == other.date and self.count == other.count


class UserDoesNotExist(Exception):
    pass


class ContributionObtainer(object):

    def _contributions_url_for_user(self, user):
        return 'https://github.com/users/{}/contributions'.format(user)

    def _contribution_from_soup_element(self, el: Tag) -> Contribution:
        date = el.attrs['data-date']
        count = int(el.attrs['data-count'])
        return Contribution(date=date, count=count)

    def _extract_contributions_from_page(self, url) -> Sequence[Contribution]:
        """
        Parses the given URL and extracts all available contributions
        """
        resp = requests.get(url)
        if resp.status_code != 200:
            raise UserDoesNotExist("User does not exist.")
        soup = BeautifulSoup(resp.text, 'html.parser')
        elements = soup.findAll('rect', class_='day')
        contributions = (self._contribution_from_soup_element(e)
                         for e in elements)
        return contributions

    def _get_contributions_for_year(self,
                                    username: str,
                                    year: int) -> Sequence[Contribution]:
        logger.info("Obtaining contributions for year {}"
                    .format(year))
        params = {
            'from': '{}-01-01'.format(year),
            'to': '{}-12-31'.format(year)
        }
        q = urlencode(params)
        url = self._contributions_url_for_user(username) + '?' + q
        return self._extract_contributions_from_page(url)

    def get_all_contributions(self, username: str) -> Sequence[Contribution]:
        """
        Obtains all of the specified user contributions
        """
        return itertools.chain(*[self._get_contributions_for_year(username, y)
                                 for y in (2014, 2015, 2016, 2017)])


if __name__ == '__main__':
    c = ContributionObtainer()
    conts = list(c.get_all_contributions('MrLokans'))
    print(list(conts))
