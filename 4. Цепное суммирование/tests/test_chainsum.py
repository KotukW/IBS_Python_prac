import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chainsum import chain_sum

def test_single_call():
    result = chain_sum(5)()
    assert result.total == 5

def test_double_call():
    result = chain_sum(5)(2)()
    assert result.total == 7

def test_triple_call():
    result = chain_sum(5)(100)(-10)()
    assert result.total == 95