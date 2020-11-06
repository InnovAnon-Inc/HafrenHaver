import pytest

#from HafrenHaver.numerology import a2n1, a2n0, a2b, a2bn1, a2bn2, a2bn11, a2bn12, a2bn21, a2bn22, numerology
from numerology import a2n1, a2n0, a2b, a2bn1, a2bn2, a2bn11, a2bn12, a2bn21, a2bn22, numerology

@pytest.mark.parametrize (
    "alpha,expected", [('IA', 91), ('FFF', 666), ('HH', 88), ('SS', 1919)]
)
def test_a2n1 (alpha, expected): assert a2n1 (alpha) == expected

# a2n0
# a2b
# a2bn1
# a2bn2
# a2bn11
# a2bn12
# a2bn21
# a2bn22
# numerology

