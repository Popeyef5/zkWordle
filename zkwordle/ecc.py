from py_ecc.bn128 import add, multiply, pairing, G1, G2

class GroupElement:

  def __init__(self, pt):
    self.pt = pt

  def __add__(self, other):
    if not isinstance(other, type(self)):
      return NotImplemented
    return type(self)(add(self.pt, other.pt))

  __radd__ = __add__

  def __mul__(self, other):
    if not isinstance(other, int):
      return NotImplemented
    return type(self)(multiply(self.pt, other))

  __rmul__ = __mul__


class bn128(GroupElement):
  pass

class bn128_2(GroupElement):
  pass

class bn128_12(GroupElement):
  pass


def e(p1, p2):
  return bn128_12(pairing(p2.pt, p1.pt))


G1 = bn128(G1)
G2 = bn128_2(G2)
