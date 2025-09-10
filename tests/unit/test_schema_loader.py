import pytest
from bench_core import loader

def test_placeholder():
    with pytest.raises(NotImplementedError):
        loader.load_and_validate([])
