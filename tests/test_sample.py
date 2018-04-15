import pytest
from .context import generator

def test_main():
    generator.__main__.main()
    assert True