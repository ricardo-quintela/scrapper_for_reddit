"""tests for the scrapper
"""
import unittest
import sys
sys.path.append("../")

from settings import APP_ID, SECRET
from utils import authenticate


class TestAuthenticate(unittest.TestCase):
    """Authentication tests
    """

    def test_authenticate(self):
        """Tests if the access token is recieved
        """
        self.assertDictEqual(authenticate(""))


if __name__ == "__main__":
    unittest.main()