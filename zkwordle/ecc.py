from py_ecc.optimized_bn128 import add, multiply, neg, pairing, G1, G2, curve_order, field_modulus

class GroupElement:

  def __init__(self, pt):
    self.pt = pt

  def __add__(self, other):
    if not isinstance(other, type(self)):
      return NotImplemented
    return type(self)(add(self.pt, other.pt))

  __radd__ = __add__

  def __iadd__(self, other):
    if not isinstance(other, type(self)):
      return NotImplemented
    self.pt = add(self.pt, other.pt)
    return self 

  def __mul__(self, other):
    if not isinstance(other, int):
      return NotImplemented
    ret = multiply(self.pt, abs(other))
    if other < 0:
      ret = neg(ret)
    return type(self)(ret)

  __rmul__ = __mul__

  def __eq__(self, other):
    if not isinstance(other, type(self)):
      return False
    return self.pt == other.pt


class bn128(GroupElement):
  pass

class bn128_2(GroupElement):
  pass


def e(p1, p2):
  return pairing(p2.pt, p1.pt)


G1 = bn128(G1)
G2 = bn128_2(G2)
