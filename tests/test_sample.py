import pytest
from .context import generator
from generator import __main__

def test_main():
    __main__.main()
    assert True