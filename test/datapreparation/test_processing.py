import pytest
from datapreparation import is_international


class TestIsInternational:
    def test_empty_string(self):
        assert is_international("") == 0

    def test_contain_inter_uppercase(self):
        assert is_international("INTER") == 1

    def test_contain_inter_lowercase(self):
        assert is_international("inter") == 1

    def test_contain_inter_camelcase(self):
        assert is_international("inter") == 1

    def test_without_international(self):
        assert is_international("abc") == 0
