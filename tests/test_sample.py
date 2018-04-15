import pytest
from .context.generator import __main__

def test_main():
    __main__.main()
    assert True