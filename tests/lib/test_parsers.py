import unittest

from lib import parsers
from lib import Transaction
from tests import helper


class ATransactionParser(unittest.TestCase):

    def setUp(self):
        self.data = helper.load_transaction_data()

    def test_can_return_all_transactions(self):
        self.parsed_data = parsers.parse_transactions(self.data)
        assert len(self.parsed_data) == 35

    def test_can_return_a_list_of_transactions(self):
        self.parsed_data = parsers.parse_transactions(self.data)
        assert isinstance(self.parsed_data, list)
        for elem in self.parsed_data:
            assert isinstance(elem, Transaction)
