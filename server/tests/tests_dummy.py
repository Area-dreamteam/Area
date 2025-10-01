import unittest

import pytest


@pytest.mark.usefixtures("db_class")
class MyTest(unittest.TestCase):
    def test_method1(self):
        assert 0, 1 - 1
